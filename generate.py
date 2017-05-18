# coding: utf-8

from datetime import datetime

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from leancloud import Object
from leancloud import Query
from leancloud.errors import LeanCloudError
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
from textwrap import *
import re
import leancloud
import urllib 
import json
from qiniu import Auth, set_default, etag, PersistentFop, build_op, op_save, Zone
from qiniu import put_data, put_file, put_stream
from qiniu import BucketManager, build_batch_copy, build_batch_rename, build_batch_move, build_batch_stat, build_batch_delete
from qiniu import urlsafe_base64_encode, urlsafe_base64_decode 
import os
# 设置 Django 项目配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

#import logging
#logging.basicConfig(level=logging.DEBUG)

APP_ID = 'xxx'
MASTER_KEY = 'xxx'

leancloud.init(APP_ID, master_key=MASTER_KEY)


class Card(Object):
    pass
class Photo(Object):
    pass    
'''
print('getting total count:')
query = Query(Card)
query.does_not_exist('photo')
count = query.count()
progress = 0
print('Total:'+str(count))
cardlist = query.find()
for card in cardlist:
    id = card.get('objectId')
    print('generating:'+id)
    result = generateCard(id)
    print('result:'+result)
    print('progess:('+str(progress)+'/'+str(count)+')')
    progress = progress+1
else:
    print('no data')

'''


def generateCard(id):
    try:
        card = Query(Card).get(id)
        tid = card.get('temlate')
        if(card.get('photo') is None):
            msstream = BytesIO()
            if tid == 1:
                template(card,msstream)
            elif tid == 2:
                template2(card,msstream)
            elif tid == 3:
                template3(card,msstream)
            elif tid == 4:
                template4(card,msstream)
            else:
                template(card,msstream)
            url = 'http://oppyrwj3t.bkt.clouddn.com';
            access_key = 'tyqeKgL8GqUmLsWKf1LVdg9RgCdgwKtRza9CEKDt'
            secret_key = 'Zc-FxrpR6Y4pVzatmdL-Pw5eA49e-szFrUiNDsj4'
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
                update = Card.create_without_data(id)
                update.set('photo',photo)
                update.save()
                return 'ok'
            else:
                return 'failed' 
        else:
            return 'already'            
    except LeanCloudError as e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            card = ''
            return 'no class' 
        else:
            raise e
            return 'error'
             

def template(card,msstream):
    w = 640
    h = 862
    iw = 600
    ih = 340
    title = card.get('name')
    content = card.get('content')
    url = card.get('img_url')
    spacing = 20
    content = fill(content, 15)
    author = '- 天天码图 -' 
    copyright = '微信小程序「天天码图」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    tw,th = draw.multiline_textsize(title, font=title_fnt)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    cw,ch = draw.multiline_textsize(content, font=content_fnt, spacing=spacing)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)
    h = 635+th+ch+crh+ah;
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)

    file = BytesIO(urllib.request.urlopen(url).read())
    photo = Image.open(file).convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>iw/ih:
        box = ((pw-ph*iw/ih)/2,0,(pw+ph*iw/ih)/2,ph)
    else:
        box = (0,(ph-pw*ih/iw)/2,pw,(ph+pw*ih/iw)/2)  

    photo = photo.crop(box)
    photo = photo.resize((iw,ih))
    base.paste(photo,box=(20,20))
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # draw text in the middle of the image, half opacity
    draw.multiline_text((w/2-tw/2,420), title, font=title_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w/2-cw/2,420+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,420+th+45+ch+115), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,420+th+45+ch+115+ah+50), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   
    
    # save image data to output stream
    base.save(msstream,"jpeg")
    # release memory
    base.close()



def template2(card,msstream):
    w = 640
    h = 1020
    iw = 600
    ih = 340
    title = card.get('name')
    content = card.get('content')
    url = card.get('img_url')
    spacing = 20
    padding = 2
    author = '- 天天码图 -' 
    copyright = '微信小程序「天天码图」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)

    file = BytesIO(urllib.request.urlopen(url).read())
    photo = Image.open(file).convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>iw/ih:
        box = ((pw-ph*iw/ih)/2,0,(pw+ph*iw/ih)/2,ph)
    else:
        box = (0,(ph-pw*ih/iw)/2,pw,(ph+pw*ih/iw)/2)  

    photo = photo.crop(box)
    photo = photo.resize((iw,ih))
    base.paste(photo,box=(20,20))
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # split the title
    tlines = wrap(title, 1)
    # current title height
    tnh = 420
    # get width and height of single title word
    stw,sth = title_fnt.getsize("已")
    for tline in tlines:       
        draw.text((w-115-stw,tnh), tline, fill=(0,0,0,255), font=title_fnt)
        tnh = tnh+sth
    # get width and height of single content word
    scw,sch = content_fnt.getsize("已")    
    clines = wrap(content, 14)
    # current width of content
    cnw = w-115-stw-115-scw
    for cline in clines:
        # current height of content 
        cnh = 420 
        cwords = wrap(cline, 1)
        for cword in cwords:
            pattern = re.compile("[，。、]+") 
            if pattern.search(cword):
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)
                # draw.text((cnw+30-12,cnh-30+12), cword, fill=(0,0,0,255), font=content_fnt)
            else:
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)                           
            cnh = cnh+sch+padding
        cnw = cnw-scw-spacing   

       
    # draw text in the middle of the image, half opacity
    # draw.multiline_text((w/2-tw/2,420), title, font=title_fnt, fill=(0,0,0,255), align='center')
    # draw.multiline_text((w/2-cw/2,420+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,h-50-15-crh-ah), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,h-15-crh), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   

    # save image data to output stream
    base.save(msstream,"jpeg")
    # release memory
    base.close()
    

def template3(card,msstream):
    w = 640
    h = 862
    iw = 600
    ih = 340
    bw = 300
    bh = 300
    title = card.get('name')
    content = card.get('content')
    url = card.get('img_url')
    spacing = 20
    content = fill(content, 15)
    author = '- 天天码图 -' 
    copyright = '微信小程序「天天码图」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    tw,th = draw.multiline_textsize(title, font=title_fnt)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    cw,ch = draw.multiline_textsize(content, font=content_fnt, spacing=spacing)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)
    h = 695+th+ch+crh+ah;
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)

    file = BytesIO(urllib.request.urlopen(url).read())
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

    base.paste(photo,box=(170,120),mask=photo)
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # draw text in the middle of the image, half opacity
    draw.multiline_text((w/2-tw/2,480), title, font=title_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w/2-cw/2,480+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,480+th+45+ch+115), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,480+th+45+ch+115+ah+50), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   
    # save image data to output stream
    base.save(msstream,"jpeg")
    # release memory
    base.close()



def template4(card,msstream):
    w = 640
    h = 1080
    iw = 600
    ih = 340
    bw = 300
    bh = 300
    padding = 2
    title = card.get('name')
    content = card.get('content')
    url = card.get('img_url')
    spacing = 20
    content = fill(content, 15)
    author = '- 天天码图 -' 
    copyright = '微信小程序「天天码图」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)

    file = BytesIO(urllib.request.urlopen(url).read())
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

    base.paste(photo,box=(170,120),mask=photo)
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # split the title
    tlines = wrap(title, 1)
    # current title height
    tnh = 480
    # get width and height of single title word
    stw,sth = title_fnt.getsize("已")
    for tline in tlines:       
        draw.text((w-115-stw,tnh), tline, fill=(0,0,0,255), font=title_fnt)
        tnh = tnh+sth
    # get width and height of single content word
    scw,sch = content_fnt.getsize("已")    
    clines = wrap(content, 14)
    # current width of content
    cnw = w-115-stw-115-scw
    for cline in clines:
        # current height of content 
        cnh = 480 
        cwords = wrap(cline, 1)
        for cword in cwords:
            pattern = re.compile("[，。、]+") 
            if pattern.search(cword):
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)
                # draw.text((cnw+30-12,cnh-30+12), cword, fill=(0,0,0,255), font=content_fnt)
            else:
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)                           
            cnh = cnh+sch+padding
        cnw = cnw-scw-spacing   

       
    # draw text in the middle of the image, half opacity
    # draw.multiline_text((w/2-tw/2,420), title, font=title_fnt, fill=(0,0,0,255), align='center')
    # draw.multiline_text((w/2-cw/2,420+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,h-50-15-crh-ah), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,h-15-crh), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   
    # save image data to output stream
    base.save(msstream,"jpeg")
    # release memory
    base.close()


print('getting total count:')
query = Query(Card)
query.does_not_exist('photo')
query.limit(1000)
count = query.count()
progress = 0
print('Total:'+str(count))
cardlist = query.find()
for card in cardlist:
    id = card.get('objectId')
    print('generating:'+id)
    result = generateCard(id)
    print('result:'+result)
    print('progess:('+str(progress)+'/'+str(count)+')')
    progress = progress+1
else:
    print('no data')
