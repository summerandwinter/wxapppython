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




# 模糊
def filter_blur(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.BLUR)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  
# 轮廓
def filter_contour(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.CONTOUR)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  
# 细节
def filter_detail(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.DETAIL)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")      
# 边缘增强
def filter_edge_enhance(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.EDGE_ENHANCE)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  

# 边缘增强
def filter_edge_enhance_more(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.EDGE_ENHANCE_MORE)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")     

# 浮雕
def filter_emboss(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.EMBOSS)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")    

#寻找边缘
def filter_find_edges(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.FIND_EDGES)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")    
#柔化
def filter_smooth(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.SMOOTH)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")     
#柔化
def filter_smooth_more(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.SMOOTH_MORE)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")   
# 锐化
def filter_sharpen(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.SHARPEN)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  
# 高斯模糊
def filter_gaussian_blur(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.GaussianBlur(4))
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")      
# 反遮罩锐化
def filter_unsharp_mask(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.UnsharpMask())
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  

def image_text(request): 
    fontSize = 40
    w = 640
    h = 640
    text = '当一艘船沉入海底\n当一个人成了谜\n你不知道\n他们为何离去\n那声再见竟是他最后一句' 
    meta = '后会无期·G.E.M.邓紫棋'
    copyright = '— 微信小程序 : 时光砂砾 —'
    # 按长度（字数）换行
    # text = fill(text,11)
    # make a blank image as the background
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    # get an image
    photo = Image.open("girl.jpg").convert('RGBA')

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


