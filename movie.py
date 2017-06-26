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
from qiniu import BucketManager, build_batch_copy, build_batch_rename, build_batch_move, build_batch_stat, build_batch_delete
from qiniu import urlsafe_base64_encode, urlsafe_base64_decode
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
from textwrap import *
import requests
from haishoku.haishoku import Haishoku
import re
import os
import base64
import json
import os

class Card(Object):
    pass
class Photo(Object):
    pass
class User(Object):
    pass  
    
class Movie():


    @staticmethod	
    def generate(card):
        try:
            if(card.get('photo') is None):
                msstream = BytesIO()
                data = {'title':card.get('name'),'content':card.get('content'),'author':card.get('author'),'url':card.get('img_url')}
                Movie.movie(data,msstream)
                url = os.environ["QINIU_ACCESS_URL"]
                access_key = os.environ["QINIU_ACCESS_KEY"]
                secret_key = os.environ["QINIU_SECRET_KEY"]
                #构建鉴权对象
                q = Auth(access_key, secret_key)
                #要上传的空间
                bucket_name = 'card'
                key = card.get('objectId')
                token = q.upload_token(bucket_name)
                ret, info = put_data(token, key, msstream.getvalue())
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
    def movie(data,msstream):
        w = 640
        h = 862
        iw = 640
        ih = 360
        content_margin_top = 60
        content_margin_bottom = 0
        title_margin_top = 10
        title_margin_bottom = 100
        max_content_w = 560
        spacing = 20
        copyright_h = 140


        title = '每日一言'
        if 'title' in data:
            title = data['title']
        title = '—《'+title+"》"    
        content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
        if 'content' in data:
            content = data['content']

        url = "https://y.gtimg.cn/music/photo_new/T001R150x150M000003CNC9D00CaVx.jpg"
        if 'url' in data:
            url = data['url']

        title_font = ImageFont.truetype('font/zh/YueSong.ttf', 26)

        title_w,title_h = title_font.getsize(title)
    
        content_formated = ''
        content_font = ImageFont.truetype('font/zh/YueSong.ttf',30)
        single_content_w,single_content_h = content_font.getsize("已")
        print(single_content_h)
        lines = content.split('\n')
        for line in lines:
            contents = list(line)
            line_formated = ''
            temp = ''
            for word in contents:
                temp += word
                temp_w,temp_h = content_font.getsize(temp)
                line_formated += word
                if temp_w + single_content_w > max_content_w:
                    line_formated += '\n'
                    temp = ''
            if temp != '':
                line_formated += '\n'
            content_formated += line_formated
    
        print(content_formated)
        
        clines = len(content_formated.split('\n'))
        content_h = clines * single_content_h + (clines -1) * spacing    


        h = ih + content_margin_top + content_h + content_margin_bottom + title_margin_top + title_h + title_margin_bottom
        #if 'id' in data and 'copyright' in data:
        #    h += copyright_h
        base = Image.new('RGBA',(w,h),(255,255,255,255))
        draw = ImageDraw.Draw(base)
        
        
        
        file = BytesIO(requests.get(url).content)
        photo = Image.open(file).convert('RGBA')
        
        (pw, ph) = photo.size
        if pw/ph>iw/ih:
            box = ((pw-ph*iw/ih)/2,0,(pw+ph*iw/ih)/2,ph)
        else:
            box = (0,(ph-pw*ih/iw)/2,pw,(ph+pw*ih/iw)/2)  
        
        photo = photo.crop(box)
        photo = photo.resize((iw,ih))
        base.paste(photo,box=(0,0))
        # get a drawing context
        draw = ImageDraw.Draw(base)
        # draw text in the middle of the image, half opacity
        draw.multiline_text((w - (title_w + w/2-max_content_w/2),ih + content_margin_top + content_h + content_margin_bottom + title_margin_top), title, font=title_font, fill=(0,0,0,255), align='right')
        draw.multiline_text((w/2-max_content_w/2,ih+content_margin_top), content_formated, font=content_font, fill=(0,0,0,255), align='left', spacing=spacing)
        
        #if 'id' in data and 'copyright' in data:
        #    wxacodestream = wx.get_wxacode_unlimit(data['id']);
        #    wxacode = Image.open(BytesIO(wxacodestream)).convert('RGBA')
        #    wxacode = wxacode.resize((copyright_h,copyright_h),Image.ANTIALIAS)
        #    base.paste(wxacode,box=(0,h-copyright_h))
        #base.show()
        # get BytesIO
        #msstream = BytesIO()
        # save image data to output stream
        base.save(msstream,"jpeg")
        # release memory
        base.close()

 
           
    @staticmethod         
    def preview(request,param):
        try:
            #param = reuest.GET.get('data')
        	json_str = base64.b64decode(param).decode('utf-8')
        	data = json.loads(json_str)
        	url = data['url']
        	title = data['title']
        	content = data['content']
        	print(content)
    
        	data = {'url':url,'title':title,'content':content}
        	msstream = BytesIO()
        	Movie.movie(data,msstream)
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
    data = {'id':'123456','url':'https://img3.doubanio.com/view/photo/photo/public/p2461588271.webp','title':'悟空传','content':content}
    msstream = BytesIO()
    Movie.movie(data,msstream)
