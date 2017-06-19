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
import requests
from haishoku.haishoku import Haishoku
import re
import os
from weixin import weixin


#app_id = os.environ["WXA_APP_ID"]
#app_secret = os.environ["WXA_APP_SECRET"] 
#wx = weixin(app_id,app_secret)  

# 模糊
def filter_blur(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.BLUR)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  
# 轮廓
def filter_contour(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.CONTOUR)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  
# 细节
def filter_detail(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.DETAIL)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")      
# 边缘增强
def filter_edge_enhance(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.EDGE_ENHANCE)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  

# 边缘增强
def filter_edge_enhance_more(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.EDGE_ENHANCE_MORE)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")     

# 浮雕
def filter_emboss(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.EMBOSS)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")    

#寻找边缘
def filter_find_edges(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.FIND_EDGES)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")    
#柔化
def filter_smooth(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.SMOOTH)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")     
#柔化
def filter_smooth_more(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.SMOOTH_MORE)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")   
# 锐化
def filter_sharpen(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.SHARPEN)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  
# 高斯模糊
def filter_gaussian_blur(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.GaussianBlur(4))
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")      
# 反遮罩锐化
def filter_unsharp_mask(request):  
    image_data = Image.open("photo.jpg")  
    fliter_data = image_data.filter(ImageFilter.UnsharpMask())
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg") 

def wxacode(request):
    
    msstream = BytesIO(wx.get_wxacode_unlimit('593351b361ff4b389e37087e'));
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")        

def template(request):
    w = 640
    h = 862
    iw = 600
    ih = 340
    title = '每日一言'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
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

    

    photo = Image.open("photo.jpg").convert('RGBA')

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
    
    wxacodestream = wx.get_wxacode_unlimit('123456');
    wxacode = Image.open(BytesIO(wxacodestream)).convert('RGBA')
    wxacode = wxacode.resize((140,140),Image.ANTIALIAS)
    base.paste(wxacode,box=(0,h-140))
    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png")  


def template2(request):
    w = 640
    h = 1020
    iw = 600
    ih = 340
    title = '每日一言'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
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


    

    photo = Image.open("photo.jpg").convert('RGBA')

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
   

    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png") 

def template3(request):
    w = 640
    h = 862
    iw = 600
    ih = 340
    bw = 300
    bh = 300
    title = '每日一言'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
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

    

    photo = Image.open("photo.jpg").convert('RGBA')

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
   

    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png") 


def template4(request):
    w = 640
    h = 1080
    iw = 600
    ih = 340
    bw = 300
    bh = 300
    padding = 2
    title = '每日一言'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
    spacing = 20
    content = fill(content, 15)
    author = '- 天天码图 -' 
    copyright = '微信小程序「天天码图」'  
    title_fnt = ImageFont.truetype('font/zh/WangQingHua.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/WangQingHua.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/WangQingHua.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/WangQingHua.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)

    

    photo = Image.open("photo.jpg").convert('RGBA')

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
   

    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png") 


def template6(request):
    w = 640
    h = 1080

    padding = 2
    spacing = 5
    title = '你还要我怎样'
    content = '我后来\n都会选择绕过那条街\n又多希望在另一条街能遇见' 
    singer = '薛之谦'
    title_fnt = ImageFont.truetype('font/zh/JunYa.otf', 35)
    singer_fnt = ImageFont.truetype('font/zh/JunYa.otf', 30)
    content_fnt = ImageFont.truetype('font/zh/WangQingHua.ttf', 30)
    clines = content.split('\n')
    mcw = 0
    for cline in clines:
        clw,clh = content_fnt.getsize(cline)
        if clw > mcw:
            mcw = clw
    ssw,ssh = singer_fnt.getsize("已")
    stw,sth = title_fnt.getsize("已")
    slines = wrap(singer, 1)
    tw,wh = title_fnt.getsize(title)
    base = Image.open("640.jpg").convert('RGBA')
    base = base.filter(ImageFilter.GaussianBlur(4))
    #base = base.filter(ImageFilter.SMOOTH)
    w, h = base.size
    draw = ImageDraw.Draw(base)
    draw.multiline_text(((w-tw)/2,100), title, font=title_fnt, fill=(255,255,255,255), align='center')
    line_height = 2
    line_width = 50
    line_padding = 10
    left_line_x = (w-tw)/2 - line_width - line_padding
    left_line_y = 100 + (sth-line_height)/2
    left_line_x2 = (w-tw)/2 - line_padding
    left_line_y2 = left_line_y

    right_line_x = (w-tw)/2 + tw + line_padding
    right_line_y = left_line_y
    right_line_x2 = (w-tw)/2 + tw + line_padding + line_width
    right_line_y2 = left_line_y
    draw.line([(left_line_x,left_line_y),(left_line_x2,left_line_y2)],fill=(255,255,255,255),width=line_height)
    draw.line([(right_line_x,right_line_y),(right_line_x2,right_line_y2)],fill=(255,255,255,255),width=line_height)
    el = int((len(slines)+1)*ssh)

    ew = el*4
    eh = el*4
    ellipse = Image.new('RGBA',(ew,eh),(255,255,255,0))
    draw2 = ImageDraw.Draw(ellipse)
    esize = 10
    for i in range(0,esize):
        draw2.ellipse([(0+i,0+i),(ew-i,eh-i)], outline=(255,255,255,255))
    ellipse = ellipse.resize((el,el),Image.ANTIALIAS)
    base.paste(ellipse,box=(int((w-el)/2),100+sth+50),mask=ellipse)
    snh = 100+sth+50+ssh/2
    for sline in slines:       
        draw.text(((w-ssw)/2,snh), sline, fill=(255,255,255,255), font=singer_fnt)
        snh = snh+ssh
    draw.multiline_text(((w-mcw)/2,320), content, font=content_fnt, fill=(255,255,255,255), align='center', spacing=spacing)
    
    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png") 

def template5(request,font):
    w = 640
    h = 1080
    iw = 600
    ih = 340
    bw = 300
    bh = 300
    padding = 2
    title = '西江月·夜行黄沙道中'
    author = '辛弃疾'
    category = '#婉约#豪放#夏天#'
    content = '''帘外雨潺潺，
春意阑珊。
罗衾不耐五更寒。
梦里不知身是客，
一晌贪欢。
独自莫凭栏，
无限江山，
别时容易见时难。
流水落花春去也，
天上人间。'''
    spacing = 20
    #content = content.replace('，','')
    #content = content.replace('。','')
    #content = content.replace('\r','。')
    #content = fill(content, 14)
    copyright = '微信小程序「天天码图」'  
    title_fnt = ImageFont.truetype('font/zh/'+font+'.ttf', 35)
    author_fnt = ImageFont.truetype('font/zh/'+font+'.ttf', 25)
    content_fnt = ImageFont.truetype('font/zh/'+font+'.ttf', 30)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 15)

    clines = content.split('\n')
    tlines = wrap(title, 1)
    alines = wrap(author, 1)
    # get width and height of single title word
    stw,sth = title_fnt.getsize("已")
    # get width and height of single content word
    saw,sah = author_fnt.getsize("已") 
    scw,sch = content_fnt.getsize("已")  
    scrw,scrh = copyright_fnt.getsize("已")
    wmh = len(tlines)*(sth+padding)
    wmw = len(clines)*(scw+spacing)
    for cline in clines:
        clineh = len(cline)*sch
        if clineh > wmh:
            wmh = clineh
    w = wmw+115+115+stw+115
    h = wmh+80+80+scrh+15
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    

    # get a drawing context
    draw = ImageDraw.Draw(base)
    # split the title
    
    # current title height
    tnh = 80 
    
    for tline in tlines:       
        draw.text((w-115-stw,tnh), tline, fill=(0,0,0,255), font=title_fnt)
        tnh = tnh+sth

    anh = 80+sah
    
    for aline in alines:       
        draw.text((w-115-stw-saw-10,anh), aline, fill=(0,0,0,255), font=author_fnt)
        anh = anh+sah    
    
    #clines = wrap(content, 14)

    # current width of content
    cnw = w-115-stw-115-scw
    lnh = 80
    for cline in clines:
        # current height of content 
        cnh = 80 
        cwords = wrap(cline, 1)
        for cword in cwords:
            if(cword != '，' and cword !='。'):
                draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)                                           
                cnh = cnh+sch+padding
            else:
                #draw.text((cnw,cnh), cword, fill=(0,0,0,255), font=content_fnt)
                cnh = cnh+sch+padding
                lnh = cnh    
        cnw = cnw-scw-spacing   
    copyrihtW,copyrightH = draw.multiline_textsize(copyright, font=copyright_fnt)    
    draw.multiline_text((w-copyrihtW,h-15-copyrightH), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
    stamp = Image.open("stamp.png").convert('RGBA')
    stamp = stamp.resize((50,50))
    base.paste(stamp,box=(cnw+scw+int((50-scw)/2),lnh-25),mask=stamp)

    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png") 

def book(request):
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

    division_left = 97*2
    division_top = title_top+single_title_h+12*2
    division = '╱'
    division_font = ImageFont.truetype('font/zh/PingFang.ttf',20*2)
    single_division_w,single_division_h = division_font.getsize("已")

    author_left = 97*2
    author_top = division_top + title_h
    author = '作者：雷蒙德.钱德勒'
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
    content_top = author_top + author_h + 12*2
    content = '故事原型：加州石油大亨爱德华.多赫尼之子被杀案，及蒂波特山油田丑闻'
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
    file = BytesIO(requests.get(url).content)
    photo = Image.open(file).convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>cover_w/cover_h:
        box = ((pw-ph*cover_w/cover_h)/2,0,(pw+ph*cover_w/cover_h)/2,ph)
    else:
        box = (0,(ph-cover_w*cover_h/cover_w)/2,pw,(ph+pw*cover_h/cover_w)/2)  

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
    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    base.save(msstream,"jpeg")
    # release memory
    base.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg") 


def music():
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
    title = '成都'
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

    division_left = 97*2
    division_top = title_top+single_title_h+12*2
    division = '╱'
    division_font = ImageFont.truetype('font/zh/PingFang.ttf',20*2)
    single_division_w,single_division_h = division_font.getsize("已")

    author_left = 97*2
    author_top = division_top + title_h
    author = '赵雷'
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
    content_top = author_top + author_h + 12*2
    content = '让我掉下眼泪的\n不止昨夜的酒\n让我依依不舍的\n不止你的温柔\n余路还要走多久\n你攥着我的手\n让我感到为难的\n是挣扎的自由'
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

    url = "https://y.gtimg.cn/music/photo_new/T002R500x500M000000jE4g74VS43p.jpg"
    file = BytesIO(requests.get(url).content)
    photo = Image.open(file).convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>cover_w/cover_h:
        box = ((pw-ph*cover_w/cover_h)/2,0,(pw+ph*cover_w/cover_h)/2,ph)
    else:
        box = (0,(ph-cover_w*cover_h/cover_w)/2,pw,(ph+pw*cover_h/cover_w)/2)  

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
    base.show()


def image_text(request): 
    fontSize = 40
    w = 640
    h = 640
    text = '当一艘船沉入海底\n当一个人成了谜\n你不知道\n他们为何离去\n那声再见竟是他最后一句' 
    meta = '后会无期·G.E.M.邓紫棋'
    copyright = '— 微信小程序 : 天天码图 —'
    # 按长度（字数）换行
    # text = fill(text,11)
    # make a blank image as the background
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    # get an image
    photo = Image.open("photo.jpg").convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>w/h:
        box = ((pw-ph)/2,0,(pw+ph)/2,ph)
    else:
        box = (0,(ph-pw)/2,pw,(pw+ph)/2)  

    photo = photo.crop(box)
    photo = photo.resize((w,h))
   
    # blur filter
    photo = photo.filter(ImageFilter.GaussianBlur())

    base.paste(photo)


    # make a blank image for text, initailized to half-transparent text color
    txt = Image.new('RGBA', (w, h), (0,0,0,100))
    # get a font
    fnt = ImageFont.truetype('font/zh/LiJin.ttf',fontSize)
    meta_fnt = ImageFont.truetype('font/zh/PingFang.ttf',20)
    copyright_fnt = ImageFont.truetype('font/zh/TongXin.ttf',14)
    # get size of the text
    # (tw, th) = fnt.getsize(text)
    # get a drawing context
    draw = ImageDraw.Draw(txt)
    tw,th = draw.multiline_textsize(text, fnt)
    mw,mh = draw.multiline_textsize(meta, meta_fnt)
    cpw,cph =draw.multiline_textsize(copyright, copyright_fnt)
    # draw text in the middle of the image, half opacity
    draw.multiline_text(((w-tw)/2,(h-th)/2), text, font=fnt, fill=(255,255,255,255), align='center',spacing=15)
    draw.multiline_text(((w-mw)/2,h-mh-30), meta, font=meta_fnt, fill=(255,255,255,150), align='center')
    draw.multiline_text(((w-cpw)/2,h-cph-10), copyright, font=copyright_fnt, fill=(255,255,255,150), align='center')

    # composite base image and text image
    out = Image.alpha_composite(base, txt)
    # get BytesIO
    msstream = BytesIO()
    # save image data to output stream
    out.save(msstream,"png")
    # release memory
    out.close()
    return HttpResponse(msstream.getvalue(),content_type="image/png")  

music()
