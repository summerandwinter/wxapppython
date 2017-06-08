import urllib  
import sys  
import http.cookiejar   
from leancloud import Object
from leancloud import Query
import json
import leancloud
import requests

APP_ID = '-gzGzoHsz'
MASTER_KEY = ''

leancloud.init(APP_ID, master_key=MASTER_KEY)

cookie = http.cookiejar.CookieJar()                                        #保存cookie，为登录后访问其它页面做准备  
cjhdr  =  urllib.request.HTTPCookieProcessor(cookie)               
opener = urllib.request.build_opener(cjhdr)  
  
  
url = "http://api.markapp.cn/v160/moviepics/everyday"  
count = 10
start = 0;
size = 80
data = {}
data['muid']= 'dVIEu/888Jh4v339tTlNfw=='
data['uid']= '23497'
r = requests.post(url, json = data)
json_obj = {}
if(r.status_code == requests.codes.ok):
	json_obj = r.json()
	print(json_obj)
else:
    print('network error')
if json_obj['status'] == 1:
	datalist = []
	Card = Object.extend('Card')    
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
		card.set('temlate',1)   
		query = Card.query
		query.equal_to('cid', int(item['id']))
		count = query.count()
		print('saving'+item['name'])
		if(count == 0):
			Card.save(card) 		 
	else:
		print('end')  
	    
else:
	print('failed') 
   

	

  