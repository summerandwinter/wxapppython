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
count = 50
start = 50  
url = "http://api.markapp.cn/v160/moviepics/more"  
data = {}
data['start'] = start
data['count'] = count
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
		query = Card.query
		query.equal_to('cid', int(item['id']))
		count = query.count()
		if(count == 0):
			print(item['name']+' '+str(item['id'])+ '不存在，获取详情...')
			detail_url = 'http://api.markapp.cn/v160/moviepics/'+str(item['id'])+'/detail'
			detail_r = requests.post(detail_url,data=data)
			if(detail_r.status_code == requests.codes.ok):
				detail_obj = detail_r.json()
				if(detail_obj['status'] == 1):
					detail = detail_obj['data']
					#print(detail)
					card = Card()
					card.set('cid',int(detail['id']))
					card.set('likes',int(detail['likes']))
					card.set('shares',int(detail['shares']))
					card.set('db_num',int(detail['db_num']))
					card.set('content',detail['content'])
					card.set('img_url',detail['img_url'])
					card.set('name',detail['name'])
					card.set('publish',True)
					card.set('template',1)
					user = User.create_without_data(userid)
					card.set('user',user)
					card.set('username',username)
					Card.save(card)
					print(item['name']+' '+str(item['id']) + '保存成功')
				else:
					print(item['name']+' '+str(item['id'])+ '详情信息获取失败')
			else:
				print(item['name']+' '+str(item['id'])+ '详情信息获取失败 网络错误')
		else:
			print(item['name']+' '+str(item['id']) + '已存在，跳过')		   			 
	else:
		print('end')  
	    
else:
	print('failed') 
   

	

  