# coding: utf-8
#!/usr/bin/python3

import pymysql
import urllib  
import sys  
import http.cookiejar   
from leancloud import Object
from leancloud import Query
import json
import leancloud


cookie = http.cookiejar.CookieJar()                                        #保存cookie，为登录后访问其它页面做准备  
cjhdr  =  urllib.request.HTTPCookieProcessor(cookie)               
opener = urllib.request.build_opener(cjhdr)  
# 打开数据库连接
db = pymysql.connect("localhost","root","root","maker",charset='utf8')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
url = "http://api.markapp.cn/v160/moviepics/more"  
count = 50
start = 0
flag = True
while flag:    
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
		#print(json_obj)
		if(len(json_obj['data']) == 0):
			flag = False
		for item in json_obj['data']:      
			sql = "INSERT INTO card(id, content, img_url, name) VALUES (%s, %s, %s, %s )" 
			try:
				cursor.execute(sql, (item['id'], item['content'], item['img_url'], item['name']))
				db.commit()
			except BaseException as e:
				print(e)
				flag = False
				db.rollback()
		else:
			print('empty')      
	else:
		print('failed') 
	start = start + 50


# 关闭数据库连接
db.close()