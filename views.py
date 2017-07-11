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
import os

class Todo(Object):
    pass

class Card(Object):
    pass
class _User(Object):
    pass    
    


def index(request):
    return render(request, 'index.html', {})


def current_time(request):
    return HttpResponse(datetime.now())

def os_info(request):
    environ = os.environ
    return HttpResponse(environ.keys(),content_type="application/json") 


def image(request):  
    image_data = Image.open("girl.jpg")  
    fliter_data = image_data.filter(ImageFilter.GaussianBlur)
    msstream=BytesIO()
    fliter_data.save(msstream,"jpeg")
    fliter_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")  

def imageNew(request):  
    image_data = Image.new('RGBA',(400,100),ImageColor.getrgb('#fff')) 
    fnt = ImageFont.truetype('font/zhanghaishan.ttf',40)
    text = 'Pillow文字示例'
    (width,height) = fnt.getsize(text)
    print(width)
    d = ImageDraw.Draw(image_data)
    d.text(((400-width)/2,(100-height)/2), text, font=fnt, fill=(0,0,0))
    msstream=BytesIO()
    image_data.save(msstream,"jpeg")
    image_data.close()
    return HttpResponse(msstream.getvalue(),content_type="image/jpeg")
          


class CardView(View):
    def get(self, request):
        page = request.GET.get('page')
        try:
            query = Query(Card)
            query.not_equal_to('publish',True)
            query.not_equal_to('deleted',True)
            query.exists('user')
            #query.not_equal_to('publish',False)
            #query.does_not_exist('cid')
            count = query.count()
            query.include('user')
            if page is None:
                page = 0
            count = query.count()
            query.skip(int(page)*100)
            query.limit(100)
            cards = query.descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:
                cards = []
            else:
                raise e
        return render(request,'cards.html',{'cards':cards,'count':count})

class CardPreviewView(View):
    def get(self, request):
        page = request.GET.get('page')
        try:
            query = Query(Card)
            query.not_equal_to('publish',True)
            query.not_equal_to('deleted',True)
            query.does_not_exist('user')
            #query.not_equal_to('publish',False)
            #query.does_not_exist('cid')
            if page is None:
                page = 0
            count = query.count()
            query.skip(int(page)*1000)
            query.limit(1000)
            query.include('user')
            cards = query.descending('likes').find()
        except LeanCloudError as e:
            if e.code == 101:
                cards = []
            else:
                raise e
        return render(request,'card_preview.html',{'cards':cards,'count':count})        

class CardPublishedView(View):
    def get(self, request):
        page = request.GET.get('page')
        try:
            query = Query(Card)
            #query.not_equal_to('publish',True)
            #query.not_equal_to('deleted',True)
            query.not_equal_to('publish',False)
            #query.does_not_exist('cid')
            count = query.count()
            query.include('user')
            if page is None:
                page = 0
            count = query.count()
            query.skip(int(page)*100)
            query.limit(100)
            cards = query.descending('publishAt').find()
        except LeanCloudError as e:
            if e.code == 101:
                cards = []
            else:
                raise e
        return render(request,'card_publish.html',{'cards':cards,'count':count})  

class CardDeletedView(View):    
    def get(self, request):
        page = request.GET.get('page')
        try:
            query = Query(Card)
            query.not_equal_to('deleted',False)
            query.does_not_exist('cid')
            query.limit(1000)
            count = query.count()
            query.include('user')
            if page is None:
                page = 0
            count = query.count()
            query.skip(int(page)*100)
            query.limit(99)
            cards = query.descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:
                cards = []
            else:
                raise e
        return render(request,'card_deleted.html',{'cards':cards,'count':count})                 

class UserView(View):
    def get(self, request):
        try:
            query = Query(_User)
            query.exists('avatarUrl')
            count = query.count()
            query.limit(1000)
            users = query.descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:
                cards = []
            else:
                raise e
        return render(request,'users.html',{'users':users,'count':count})              

class TodoView(View):
    def get(self, request):
        try:
            todos = Query(Todo).descending('createdAt').find()
        except LeanCloudError as e:
            if e.code == 101:  # 服务端对应的 Class 还没创建
                todos = []
            else:
                raise e
        return render(request, 'todos.html', {
            'todos': [x.get('content') for x in todos],
        })

    def post(self, request):
        content = request.POST.get('content')
        todo = Todo(content=content)
        try:
            todo.save()
        except LeanCloudError as e:
            return HttpResponseServerError(e.error)
        return HttpResponseRedirect(reverse('todo_list'))
