import urllib  
import sys  
import http.cookiejar   
from leancloud import Object
from leancloud import Query
import json
import leancloud

APP_ID = 'xxx'
MASTER_KEY = 'xxx'

leancloud.init(APP_ID, master_key=MASTER_KEY)
cookie = http.cookiejar.CookieJar()                                        #保存cookie，为登录后访问其它页面做准备  
cjhdr  =  urllib.request.HTTPCookieProcessor(cookie)               
opener = urllib.request.build_opener(cjhdr)  
  
  
url = "http://api.markapp.cn/v160/moviepics/more"  
count = 10
start = 0;
size = 80
while start < 800:    
	data={}
	data['count']=count
	data['muid']= 'dVIEu/888Jh4v339tTlNfw=='
	data['uid']= '23497'
	data['start']= start
	postdata = urllib.parse.urlencode(data)  
	postdata = postdata.encode('utf-8')  
	res = urllib.request.urlopen(url,postdata)
	string = res.read().decode('utf-8')
	json_obj = json.loads(string)  
	if json_obj['status'] == 1:
		datalist = []
		Card = Object.extend('Card')    
		for item in json_obj['data']:    
			card = Card()
			card.set('id',item['id'])    
			card.set('content',item['content'])   
			card.set('img_url',item['img_url'])    
			card.set('name',item['name'])    
			datalist.append(card)
		else:
			print('empty')  
		Card.save_all(datalist)      
	else:
		print('failed') 
	start = start + 10
    

  