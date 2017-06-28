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

class Card(Object):
    pass
class Photo(Object):
    pass
class User(Object):
    pass  
    
class Book():

    @staticmethod	
    def generate(card):
        try:
            if(card.get('photo') is None):
                msstream = BytesIO()
                data = {'title':card.get('name'),'content':card.get('content'),'author':card.get('author'),'url':card.get('img_url')}
                Book.book(data,msstream)
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
    def book(data,msstream):
        w = 490*2
        h = 740*2
        banner_w = 490*2
        banner_h = 265*2
        cover_w = 135*2
        cover_h = 200*2
        cover_top = 120*2
        cover_left = int((w-cover_w)/2)
        block_w = 32*2
        block_h = 12*2
        block_left = 97*2
        block_top = 160*2 + banner_h
        max_content_w = 310*2

        title_left = 97*2
        title_top = block_top+block_h+20*2 
        title = '高窗'
        if 'title' in data:
    	    title = data['title']

        title_font = ImageFont.truetype('font/zh/YueSong.ttf',28*2)
        single_title_w,single_title_h= title_font.getsize("已")
        titles = wrap(title, 1)
        title_formated = ''
        temp = ''
        for word in titles:
            temp += word
            temp_w,temp_h = title_font.getsize(temp)
            title_formated += word
            if temp_w > max_content_w + single_title_w:
                title_formated +=  '\n'
                temp = ''
        tlines = len(title_formated.split('\n'))
        title_h = tlines * single_title_h + (tlines -1) * 28*2

        division_left = 99*2
        division_top = title_top+single_title_h+12*2
        division = '╱'
        division_font = ImageFont.truetype('font/zh/PingFang.ttf',20*2)
        single_division_w,single_division_h = division_font.getsize("已")

        author_left = 97*2
        author_top = division_top + single_division_h +12*2
        author = '雷蒙德.钱德勒'
        if 'author' in data:
    	    author = data['author']
        author = '作者：' + author    
        author_font = ImageFont.truetype('font/zh/YueSong.ttf',14*2)
        single_author_w,single_author_h = author_font.getsize("已")
        authors = wrap(author, 1)
        author_formated = ''
        temp = ''
        for word in authors:
            temp += word
            temp_w,temp_h = author_font.getsize(temp)
            author_formated += word
            if temp_w > max_content_w + single_author_w:
                author_formated +=  '\n'
                temp = ''
        alines = len(author_formated.split('\n'))
        author_h = alines * single_author_h + (alines -1) * 14*2

        content_left = 97*2
        content_top = author_top + author_h + 16*2
        content = '故事原型：加州石油大亨爱德华.多赫尼之子被杀案，及蒂波特山油田丑闻'
        if 'content' in data:
    	    content = data['content']
        content_formated = ''
        content_font = ImageFont.truetype('font/zh/YueSong.ttf',14*2)
        single_content_w,single_content_h = content_font.getsize("已")
        contents = wrap(content, 1)
        temp = ''
        for word in contents:
            temp += word
            temp_w,temp_h = content_font.getsize(temp)
            content_formated += word
            if temp_w > max_content_w + single_content_w:
                content_formated +=  '\n'
                temp = ''

        print(content_formated)
    
        clines = len(content_formated.split('\n'))
        content_h = clines * single_author_h + (clines -1) * 14*2
        h = content_top + content_h + 150*2

        base = Image.new('RGBA',(w,h),(255,255,255,255))
        draw = ImageDraw.Draw(base)
        draw.rectangle([(0,0),(banner_w,banner_h)],(26, 26, 26, 255))

        url = "https://img3.doubanio.com/lpic/s27028282.jpg"
        if 'url' in data:
    	    url = data['url']
        file = BytesIO(requests.get(url).content)
        photo = Image.open(file).convert('RGBA')

        (pw, ph) = photo.size
        if pw/ph>cover_w/cover_h:
            box = ((pw-ph*cover_w/cover_h)/2,0,(pw+ph*cover_w/cover_h)/2,ph)
        else:
            box = (0,(ph-pw*cover_h/cover_w)/2,pw,(ph+pw*cover_h/cover_w)/2)  

        photo = photo.crop(box)
        photo = photo.resize((cover_w,cover_h),Image.ANTIALIAS)
        base.paste(photo,box=(cover_left,cover_top))

        dominant = Haishoku.getDominant(file)

        draw.rectangle([(block_left,block_top),(block_left+block_w,block_top+block_h)],dominant)
        draw.multiline_text((title_left,title_top), title_formated, font=title_font, fill=(70,70,70), align='left',spacing=15*2)
        draw.multiline_text((division_left,division_top), division, font=division_font, fill=(70,70,70), align='left',spacing=0)
        draw.multiline_text((author_left,author_top), author_formated, font=author_font, fill=(90,90,90), align='left',spacing=15*2)
        draw.multiline_text((content_left,content_top), content_formated, font=content_font, fill=(90,90,90), align='left',spacing=12*2)
        print(dominant)
        #base.show()

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
        	author = data['author']
        	content = data['content']
        	print(content)
    
        	data = {'url':url,'title':title,'author':author,'content':content}
        	msstream = BytesIO()
        	Book.book(data,msstream)
        	return HttpResponse(msstream.getvalue(),content_type="image/png") 
        except LeanCloudError as e:
            if e.code == 101:  # 服务端对应的 Class 还没创建
                card = ''
                return HttpResponse(e,content_type="text/plain") 
            else:
                raise e
                return HttpResponse(e,content_type="text/plain")
    
    
if __name__ == "__main__":
    data = {}
    msstream = BytesIO()
    Book.book(data,msstream)     