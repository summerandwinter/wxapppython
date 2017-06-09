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
# SQL 查询语句
sql = "SELECT * FROM card "
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      cid = row[0]
      data={}
      data['muid']= 'dVIEu/888Jh4v339tTlNfw=='
      data['uid']= '23497'
      url = 'http://api.markapp.cn/v160/moviepics/'+str(cid)+'/detail'
      postdata = urllib.parse.urlencode(data)  
      postdata = postdata.encode('utf-8')
      res = urllib.request.urlopen(url,postdata)
      string = res.read().decode('utf-8')
      json_obj = json.loads(string)
      if json_obj['status'] == 1:
          item = json_obj['data']
          sqlupdate = "UPDATE card SET content = %s, likes = %s, shares = %s, db_num = %s WHERE id = %s"
          try:
              cursor.execute(sqlupdate, (item['content'], item['likes'], item['shares'], item['db_num'],item['id']))
              db.commit()
          except BaseException as e: 
          	print(e)
          	db.rollback()
       # 打印结果
      print (cid)
except BaseException as e: 
    print(e)
    print ("Error: unable to fetch data")

# 关闭数据库连接
db.close()