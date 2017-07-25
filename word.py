# coding: utf-8

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from leancloud import Object
from leancloud import Query
from leancloud.errors import LeanCloudError
from qiniu import Auth, set_default, etag, PersistentFop, build_op, op_save, Zone
from qiniu import put_data, put_file, put_stream
from qiniu import BucketManager,CdnManager, build_batch_copy, build_batch_rename, build_batch_move, build_batch_stat, build_batch_delete
from qiniu import urlsafe_base64_encode, urlsafe_base64_decode
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
from textwrap import *
from weixin import weixin
from util import Util
import requests
from haishoku.haishoku import Haishoku
import re
import os
import base64
import json
import os
import configparser 

cf = configparser.ConfigParser()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
cf.read("config.conf")
os.environ["WXA_APP_ID"] = cf.get("wxa", "app_id")
os.environ["WXA_APP_SECRET"] = cf.get("wxa", "app_secret")
app_id = os.environ["WXA_APP_ID"]
app_secret = os.environ["WXA_APP_SECRET"]
wx = weixin(app_id,app_secret)
class Card(Object):
    pass
class Photo(Object):
    pass
class User(Object):
    pass  
    
class Word():


    @staticmethod	
    def generate(card):
        try:
            
            msstream = BytesIO()
            template = card.get('template')
            data = {'id':card.id,'title':card.get('name'),'content':card.get('content'),'author':card.get('author'),'url':card.get('img_url')}
            if template == 1:
                Word.template(data,msstream)
            elif template == 3:
                Word.template3(data,msstream)
            else:
                Word.template(data,msstream)       
            url = os.environ["QINIU_ACCESS_URL"]
            access_key = os.environ["QINIU_ACCESS_KEY"]
            secret_key = os.environ["QINIU_SECRET_KEY"]
            #构建鉴权对象
            q = Auth(access_key, secret_key)
            #要上传的空间
            bucket_name = 'card'
            key = card.get('objectId')
            if card.get('photo') is None:
                token = q.upload_token(bucket_name)
                ret, info = put_data(token, key, msstream.getvalue())
            else:
                cdn_manager = CdnManager(q)
                urls = ['http://oppyrwj3t.bkt.clouddn.com/'+key]
                token = q.upload_token(bucket_name,key)
                ret, info = put_data(token, key, msstream.getvalue())
                refresh_url_result = cdn_manager.refresh_urls(urls)
            
            if(info.ok()):
                metaData = {'owner':card.get('username')}
                photo = Photo() 
                photo.set('mine_type','image/jpeg')
                photo.set('key',key)
                photo.set('name',key)
                photo.set('url',url+'/'+key)
                photo.set('provider','qiniu')
                photo.set('metaData',metaData)
                photo.set('bucket',bucket_name)
                photo.save()
                update = Card.create_without_data(key)
                update.set('photo',photo)
                update.save()
                return 'ok'
            else:
                return 'failed'
            return 'already'
                   
                
        except LeanCloudError as e:
            if e.code == 101:  # 服务端对应的 Class 还没创建
                card = ''
                return HttpResponse(e,content_type="text/plain") 
            else:
                raise e
                return HttpResponse(e,content_type="text/plain")

    @staticmethod
    def template(data,msstream):
        w = 640
        h = 640
        iw = 600
        ih = 340
        title = ''
        if 'title' in data:
            title = data['title']
        content = ''
        if 'content' in data:
            content = data['content']

        url = ''
        if 'url' in data:
            url = data['url']
   
        spacing = 20
        max_content_w = 420
        padding_top = 100
        padding_bottom = 100
        content_padding_top = 45
        author_padding_top = 70
        author = ''
        if 'author' in data:
            author = '- '+data['author']+' -' 

        copyright = '微信小程序「天天码图」'  
        title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
        content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 28)
        author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 20)
        copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 20)
        content_formated = Util.content_format(content,content_fnt,max_content_w)

        single_content_w,single_content_h = content_fnt.getsize("已")
        
    
        print(content_formated)
             

        #compute the height of the text area
        text_w = 420
        text_h = 0
        clines = len(content_formated.split('\n'))
     
        content_h = clines * single_content_h + (clines -1) * spacing

        tw = 0
        th = 0    
        if len(title) > 0:
            tw,th = title_fnt.getsize(title)
            text_h += th + content_padding_top
        text_h += content_h 
        aw = 0
        ah = 0
        if len(author)>0:
            aw,ah = author_fnt.getsize(author)
            text_h += ah + author_padding_top
        
        
        text = Image.new('RGBA',(text_w,text_h),(255,255,255,255))

        draw = ImageDraw.Draw(text)
        # draw text in the middle of the image, half opacity
        content_top = 0
        if len(title) > 0:
            draw.multiline_text((text_w/2-tw/2,0), title, font=title_fnt, fill=(0,0,0,255), align='center')
            content_top = content_top + th + content_padding_top
        draw.multiline_text((0,content_top), content_formated, font=content_fnt, fill=(0,0,0,255), align='left', spacing=spacing)
        author_top = content_top + content_h +author_padding_top

        if len(author) > 0:
            draw.multiline_text((text_w/2-aw/2,author_top), author, font=author_fnt, fill=(0,0,0,255), align='center')

        crw,crh = copyright_fnt.getsize(copyright)

        h = max(text_h + padding_top +padding_bottom,h)       
        text_padding_top = 40
        text_padding_bottom = 80
        if url != '':
            h = max(ih + 20 + text_padding_top + text_padding_bottom + text_h,h)

        base = Image.new('RGBA',(w,h),(255,255,255,255))
        draw = ImageDraw.Draw(base)
        text_left = int((w-text_w)/2)
        text_top = int((h-text_h)/2)
        if url !='':
            file = BytesIO(requests.get(url).content)
            photo = Image.open(file).convert('RGBA')
            text_top = ih + 20 + text_padding_top 
            (pw, ph) = photo.size
            if pw/ph>iw/ih:
                box = ((pw-ph*iw/ih)/2,0,(pw+ph*iw/ih)/2,ph)
            else:
                box = (0,(ph-pw*ih/iw)/2,pw,(ph+pw*ih/iw)/2)  
    
            photo = photo.crop(box)
            photo = photo.resize((iw,ih))
            base.paste(photo,box=(20,20))
        # get a drawing context
        base.paste(text,box=(text_left,text_top))
        draw.multiline_text((w-crw,h-crh-10), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
       
        
        # save image data to output stream
        base.save(msstream,"jpeg")
        #base.show()
        # release memory
        base.close()
    
    @staticmethod
    def template3(data,msstream):
        w = 640
        h = 640
        iw = 600
        ih = 340
        bw = 300
        bh = 300        
        title = ''
        if 'title' in data:
            title = data['title']
        content = ''
        if 'content' in data:
            content = data['content']

        url = ''
        if 'url' in data:
            url = data['url']
   
        spacing = 20
        max_content_w = 420
        padding_top = 100
        padding_bottom = 100
        content_padding_top = 45
        author_padding_top = 70
        author = ''
        if 'author' in data:
            author = '- '+data['author']+' -' 

        copyright = '微信小程序「天天码图」'  
        title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
        content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 28)
        author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 20)
        copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 20)
        content_formated = Util.content_format(content,content_fnt,max_content_w)

        single_content_w,single_content_h = content_fnt.getsize("已")
        
    
        print(content_formated)
             

        #compute the height of the text area
        text_w = 420
        text_h = 0
        clines = len(content_formated.split('\n'))
     
        content_h = clines * single_content_h + (clines -1) * spacing

        tw = 0
        th = 0    
        if len(title) > 0:
            tw,th = title_fnt.getsize(title)
            text_h += th + content_padding_top
        text_h += content_h 
        aw = 0
        ah = 0
        if len(author)>0:
            aw,ah = author_fnt.getsize(author)
            text_h += ah + author_padding_top
        
        
        text = Image.new('RGBA',(text_w,text_h),(255,255,255,255))

        draw = ImageDraw.Draw(text)
        # draw text in the middle of the image, half opacity
        content_top = 0
        if len(title) > 0:
            draw.multiline_text((text_w/2-tw/2,0), title, font=title_fnt, fill=(0,0,0,255), align='center')
            content_top = content_top + th + content_padding_top
        draw.multiline_text((0,content_top), content_formated, font=content_fnt, fill=(0,0,0,255), align='left', spacing=spacing)
        author_top = content_top + content_h +author_padding_top

        if len(author) > 0:
            draw.multiline_text((text_w/2-aw/2,author_top), author, font=author_fnt, fill=(0,0,0,255), align='center')

        crw,crh = copyright_fnt.getsize(copyright)

        h = max(text_h + padding_top +padding_bottom,h)       
        text_padding_top = 60
        text_padding_bottom = 80
        photo_padding_top = 110
        if url != '':
            h = bh + photo_padding_top + text_padding_top + text_padding_bottom + text_h

        base = Image.new('RGBA',(w,h),(255,255,255,255))
        
        text_left = int((w-text_w)/2)
        text_top = int((h-text_h)/2)
        if url !='':
            text_top = bh + photo_padding_top + text_padding_top
            file = BytesIO(requests.get(url).content)
            photo = Image.open(file).convert('RGBA')
    
            pw, ph = photo.size
    
            if pw > ph:
                box = ((pw-ph*bw/bh)/2,0,(pw+ph*bw/bh)/2,ph)
            else:
                box = (0,(ph-pw*bh/bw)/2,pw,(ph+pw*bh/bw)/2)  
    
            photo = photo.crop(box)
            photo = photo.resize((bw*4,bh*4))
    
            circle = Image.new('L', (bw*4, bh*4), 0)
            draw = ImageDraw.Draw(circle)
            draw.ellipse((0, 0, bw*4, bh*4), fill=255)
            alpha = Image.new('L', (bw*4, bh*4), 255)
            alpha.paste(circle, (0, 0))
            photo.putalpha(alpha)
            photo = photo.resize((bw,bh),Image.ANTIALIAS)
        box_left = int((w-bw)/2)
        box_top = photo_padding_top
        base.paste(photo,box=(box_left,box_top),mask=photo)
        # get a drawing context
        base.paste(text,box=(text_left,text_top))
        draw = ImageDraw.Draw(base)
        draw.multiline_text((w-crw,h-crh-10), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
       
        
        # save image data to output stream
        base.save(msstream,"jpeg")
        #base.show()
        # release memory
        base.close()    
        

    
    

           
    @staticmethod         
    def preview(request,param):
        try:
            #param = reuest.GET.get('data')
            json_str = base64.b64decode(param).decode('utf-8')
            json_data = json.loads(json_str)
            data = {'content':json_data['content']}
            if 'url' in json_data:
                data['url'] = json_data['url']
            if 'title' in json_data:
                data['title'] = json_data['title']
            if 'author' in json_data:
                data['author'] = json_data['author']
            msstream = BytesIO()
            Word.template(data,msstream)
            return HttpResponse(msstream.getvalue(),content_type="image/png") 
        except LeanCloudError as e:
            if e.code == 101:  # 服务端对应的 Class 还没创建
                card = ''
                return HttpResponse(e,content_type="text/plain") 
            else:
                raise e
                return HttpResponse(e,content_type="text/plain")
    
if __name__ == "__main__":
    content = '我要这天，再遮不住我眼，要这地，再埋不了我心，要这众生，都明白我意，要那诸佛，都烟消云散！'
    data = {'author':'今何在','title':'悟空传','content':content,'url':'https://img3.doubanio.com/view/photo/photo/public/p2461588271.webp'}
    msstream = BytesIO()
    Word.template3(data,msstream)
