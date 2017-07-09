# coding: utf-8
#!/usr/bin/python3

import pymysql
import sys  

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
    content_list = []
    for row in results:
        id = row[0]
        content = row[1]
        img_url = row[2]
        name = row[3]
        db_num = row[4]
        likes = row[5]
        shares = row[6]
        if content not in content_list:
        	sql_insert = "INSERT INTO card2(id, content, img_url, name,likes,shares,db_num) VALUES (%s, %s, %s, %s, %s, %s, %s  )" 
        	cursor.execute(sql_insert, (id,content,img_url,name,likes, shares, db_num))
        	db.commit()
        	print(content)
        	content_list.append(content)
except BaseException as e:
    print(e)
    db.rollback() 
db.close()    
  
