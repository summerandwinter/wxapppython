import urllib  
import sys  
import http.cookiejar   
from leancloud import Object
from leancloud import Query
import json
import leancloud
import requests

APP_ID = '7C7MfP24LboNSLeOnbh112nT-gzGzoHsz'
MASTER_KEY = 'bIEoNy5pSWoqvC3qq0vpGMT1'

leancloud.init(APP_ID, master_key=MASTER_KEY)

cookie = http.cookiejar.CookieJar()                                        #保存cookie，为登录后访问其它页面做准备  
cjhdr  =  urllib.request.HTTPCookieProcessor(cookie)               
opener = urllib.request.build_opener(cjhdr)  
  
userid = '590be679ac502e006cdc63c0'
username = '569dil3zuypnrpjqwe97l3qkw'  
url = "http://api.markapp.cn/v160/moviepics/everyday"  
data = {}
data['muid']= 'dVIEu/888Jh4v339tTlNfw=='
data['uid']= '23497'
r = requests.post(url, data = data)
json_obj = {}
if(r.status_code == requests.codes.ok):
	json_obj = r.json()
	#print(json_obj)
else:
    print('network error')
if json_obj['status'] == 1:
	datalist = []
	Card = Object.extend('Card')  
	User = Object.extend('_User')  
	for item in json_obj['data']:    
		card = Card()
		card.set('cid',int(item['id'])) 
		card.set('likes',int(item['likes']))    
		card.set('shares',int(item['shares']))   
		card.set('db_num',int(item['db_num']))       
		card.set('content',item['content'])   
		card.set('img_url',item['img_url'])    
		card.set('name',item['name']) 
		card.set('publish',True) 
		card.set('template',1)
		user = User.create_without_data(userid)
		card.set('user',user)
		card.set('username',username)
		query = Card.query
		query.equal_to('cid', int(item['id']))
		count = query.count()
		#print('saving'+item['name'])
		if(count == 0):
			Card.save(card)
			print(item['name']+' 保存成功')
		else:
		    print(item['name']+' 已存在，跳过') 		 
	else:
		print('end')  
	    
else:
	print('failed') 
   

	

  