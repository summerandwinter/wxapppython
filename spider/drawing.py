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
Doodle = Object.extend('Doodle')
leancloud.init(APP_ID, master_key=MASTER_KEY)

cookie = http.cookiejar.CookieJar()                                        #保存cookie，为登录后访问其它页面做准备  
cjhdr  =  urllib.request.HTTPCookieProcessor(cookie)               
opener = urllib.request.build_opener(cjhdr)  
  
openid = 'otR84wd8PgOyOz_V9GW05Q_6oJDQ'
for id in range(1,423): 
    url = "https://drawing.api.sdningrun.com/path/getOne"  
    data = {}
    data['openid']= openid
    data['id']= id
    r = requests.post(url, data = data)
    json_obj = {}
    if(r.status_code == requests.codes.ok):
        json_obj = r.json()
        if json_obj['status'] == 200:
            if json_obj['data'] is not None:
                dodle = Doodle()
                data = json_obj['data']
                dodle.set('cid',int(id))
                dodle.set('path',data['path']) 
                dodle.set('pic',data['pic'])
                Doodle.save(dodle)
                print(str(id) + ' saved',flush=True)
            else:
                print(str(id) + ' no data',flush=True)
    else:
        print('network error')

         	    
    