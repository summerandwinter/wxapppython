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

def detail(cid):
    data={}
    db = pymysql.connect("localhost","root","root","maker",charset='utf8')
    cursor = db.cursor()

    data['muid']= 'i//7bo3rkEgkceEpcKw19Q=='
    data['uid']= '543813'
    url = 'http://api.markapp.cn/v160/moviepics/'+str(cid)+'/detail'
    postdata = urllib.parse.urlencode(data)  
    postdata = postdata.encode('utf-8')
    
    res = urllib.request.urlopen(url,postdata,timeout=3)
    
    string = res.read().decode('utf-8')
    json_obj = json.loads(string)
    if json_obj['status'] == 1:
    	if json_obj['data'] is not None:
    		item = json_obj['data']
    		sql = "INSERT INTO card(id, content, img_url, name,likes,shares,db_num) VALUES (%s, %s, %s, %s, %s, %s, %s  )" 
    		try:
    			cursor.execute(sql, (item['id'],item['content'],item['img_url'],item['name'],item['likes'], item['shares'], item['db_num']))
    			db.commit()
    			print('保存成功')
    		except BaseException as e:
    			print(e)
    			db.rollback()
    	else:
    		print(json_obj['data'])    	
    else:
    	print(json_obj['data'])
    db.close()	
#detail(40)

# SQL 查询语句
sql = "SELECT * FROM card "
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    id_list = []
    for row in results:
        cid = row[0]
        id_list.append(cid)
except BaseException as e:
    print(e)
    db.rollback() 
db.close()    
for i in range(14,130694):
	if(i not in id_list):
		print(i)
		try:
		    detail(i)
		except Exception as e:
			print(str(e))
			continue    
