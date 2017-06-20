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
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
from textwrap import *
import requests
from haishoku.haishoku import Haishoku
import re
import os
import base64
import json

def music(data,msstream):
    w = 490*2
    h = 740*2
    banner_w = 490*2
    banner_h = 265*2
    cover_w = 200*2
    cover_h = 200*2
    cover_top = 120*2
    cover_left = 100*2
    block_w = 32*2
    block_h = 12*2
    block_left = 97*2
    block_top = 160*2 + banner_h
    max_content_w = 300*2

    max_title_w = 190*2
    title_left = cover_w + cover_left + 10 *2

    title = '成都'
    if data['title']:
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
        if temp_w > max_title_w + single_title_w:
            title_formated +=  '\n'
            temp = ''
    tlines = len(title_formated.split('\n'))
    title_h = tlines * single_title_h + (tlines -1) * 28*2
    title_top = banner_h - title_h - 10 *2

    max_author_w = 190*2
    author_left = cover_w + cover_left+ 10 *2
    author_top = banner_h + 10 *2
    author = '赵雷'
    if data['author']:
    	author = data['author']
    author_font = ImageFont.truetype('font/zh/YueSong.ttf',14*2)
    single_author_w,single_author_h = author_font.getsize("已")
    authors = wrap(author, 1)
    author_formated = ''
    temp = ''
    for word in authors:
        temp += word
        temp_w,temp_h = author_font.getsize(temp)
        author_formated += word
        if temp_w > max_author_w + single_author_w:
            author_formated +=  '\n'
            temp = ''
    alines = len(author_formated.split('\n'))
    author_h = alines * single_author_h + (alines -1) * 14*2

    content_left = 95*2
    content_top = banner_h + 150*2
    content = '让我掉下眼泪的\n不止昨夜的酒\n让我依依不舍的\n不止你的温柔\n余路还要走多久\n你攥着我的手\n让我感到为难的\n是挣扎的自由'
    if data['content']:
    	content = data['content']
    content_formated = ''
    content_font = ImageFont.truetype('font/zh/YueSong.ttf',18*2)
    single_content_w,single_content_h = content_font.getsize("已")
    lines = content.split('\n')
    for line in lines:
        contents = wrap(line, 1)
        line_formated = ''
        temp = ''
        for word in contents:
            temp += word
            temp_w,temp_h = content_font.getsize(temp)
            line_formated += word
            if temp_w > max_content_w + single_content_w:
                line_formated += '\n'
                temp = ''
        if temp != '':
            line_formated += '\n'
        content_formated += line_formated

    print(content_formated)
    
    clines = len(content_formated.split('\n'))
    content_h = clines * single_author_h + (clines -1) * 14*2
    h = content_top + content_h + 100*2

    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    

    url = "https://y.gtimg.cn/music/photo_new/T002R500x500M000000jE4g74VS43p.jpg"
    if data['url']:
    	url = data['url']
    file = BytesIO(requests.get(url).content)
    photo = Image.open(file).convert('RGBA')
    (pw, ph) = photo.size



    if pw/ph>w/h:
        bbox = ((pw-ph*w/h)/2,0,(pw+ph*w/h)/2,ph)
    else:
        bbox = (0,(ph-pw*h/w)/2,pw,(ph+pw*h/w)/2)        

    banner_cover = photo.crop(bbox)
    banner_cover = banner_cover.resize((w,h),Image.ANTIALIAS)
    banner_cover = banner_cover.filter(ImageFilter.GaussianBlur(60))
    banner_wrap = Image.new('RGBA',(w,h),(255, 255, 255, 125))
    banner_cover = Image.alpha_composite(banner_cover,banner_wrap)
    base.paste(banner_cover,box=(0,0))

    
    if pw/ph>cover_w/cover_h:
        box = ((pw-ph*cover_w/cover_h)/2,0,(pw+ph*cover_w/cover_h)/2,ph)
    else:
        box = (0,(ph-pw*cover_h/cover_w)/2,pw,(ph+pw*cover_h/cover_w)/2)

    cover = photo.crop(box)
    cover = cover.resize((cover_w,cover_h),Image.ANTIALIAS)
    base.paste(cover,box=(cover_left,cover_top))
  
    draw.multiline_text((title_left,title_top), title_formated, font=title_font, fill=(0,0,0), align='left',spacing=15*2)
    draw.multiline_text((author_left,author_top), author_formated, font=author_font, fill=(10,10,10), align='left',spacing=15*2)
    draw.multiline_text((content_left,content_top), content_formated, font=content_font, fill=(0,0,0), align='left',spacing=12*2)
    #base.show()

    # save image data to output stream
    base.save(msstream,"jpeg")
    # release memory
    base.close()
       
             
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
    	music(data,msstream)
    	return HttpResponse(msstream.getvalue(),content_type="image/png") 
    except LeanCloudError as e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            card = ''
            return HttpResponse(e,content_type="text/plain") 
        else:
            raise e
            return HttpResponse(e,content_type="text/plain")


