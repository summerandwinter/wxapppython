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
import re
import leancloud
import urllib 
import json
from qiniu import Auth, set_default, etag, PersistentFop, build_op, op_save, Zone
from qiniu import put_data, put_file, put_stream
from qiniu import BucketManager, build_batch_copy, build_batch_rename, build_batch_move, build_batch_stat, build_batch_delete
from qiniu import urlsafe_base64_encode, urlsafe_base64_decode 
import os
import configparser 

cf = configparser.ConfigParser() 
cf.read("config.conf") 
os.environ["WXA_APP_ID"] = cf.get("wxa", "app_id") 
os.environ["WXA_APP_SECRET"] = cf.get("wxa", "app_secret") 
os.environ["QINIU_ACCESS_KEY"] = cf.get("qiniu", "access_key") 
os.environ["QINIU_SECRET_KEY"] = cf.get("qiniu", "secret_key")
os.environ["QINIU_ACCESS_URL"] = cf.get("qiniu", "access_url")  

APP_ID = '7C7MfP24LboNSLeOnbh112nT-gzGzoHsz'
MASTER_KEY = 'bIEoNy5pSWoqvC3qq0vpGMT1'

leancloud.init(APP_ID, master_key=MASTER_KEY)

class Card(Object):
    pass
class Photo(Object):
    pass  
class _User(Object):
    pass      
class _File(Object):
	pass


print('getting total count:')
query = Query(_File)

query.limit(100)
count = query.count()
print('Total:'+str(count))
filelist = query.find()
cardquery = Card.query
for file in filelist:
    meta = file.get('metaData')
    username = meta['owner']
    url = file.get('url')
    
    cardquery.equal_to('img_url',url)
    count = cardquery.count()

    if(count>0):
    	card = cardquery.first()
    	data = Card.create_without_data(card.get('objectId'))
    	data.set('username',username)
    	data.save()
    	print(card.get('objectId'))
    #user = userquery.first()
    #print(user.get('id'))
    #print(card)
    print(username)
    
else:
    print('end')


