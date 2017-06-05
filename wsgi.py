# coding: utf-8

from gevent import monkey
monkey.patch_all()

import os
import configparser 
# 设置 Django 项目配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import leancloud
from gevent.pywsgi import WSGIServer

from cloud import engine
cf = configparser.ConfigParser() 
cf.read("config.conf") 
os.environ["WX_APP_ID"] = cf.get("wx", "app_id") 
os.environ["WX_APP_SECRET"] = cf.get("wx", "app_secret") 
os.environ["WXA_APP_ID"] = cf.get("wxa", "app_id") 
os.environ["WXA_APP_SECRET"] = cf.get("wxa", "app_secret") 
os.environ["QINIU_ACCESS_KEY"] = cf.get("qiniu", "access_key") 
os.environ["QINIU_SECRET_KEY"] = cf.get("qiniu", "secret_key")
os.environ["QINIU_ACCESS_URL"] = cf.get("qiniu", "access_url")  
#import logging
#logging.basicConfig(level=logging.DEBUG)

APP_ID = os.environ['LC_APP_ID']
MASTER_KEY = os.environ['LC_APP_MASTER_KEY']
PORT = int(os.environ['LC_APP_PORT'])

leancloud.init(APP_ID, master_key=MASTER_KEY)

application = engine


if __name__ == '__main__':
    # 只在本地开发环境执行的代码
    server = WSGIServer(('localhost', PORT), application)
    server.serve_forever()
