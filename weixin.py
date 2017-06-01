#coding: utf8  
from django.core.cache import cache
from io import BytesIO
import requests
import os
TOKEN_KEY = 'ACCESS_TOKKEN'
class weixin():
	def __init__(self,appid,app_secret):
		self.appid = appid
		self.app_secret = app_secret

	def get_token(self):
	    token_cache_key = TOKEN_KEY
	    token = cache.get(token_cache_key)
	    if(token):
	        return token
	    else:
	        dict_data = self.get_access_token()
	        token = dict_data.get('access_token')
	        expires_in = dict_data.get('expires_in')
	        if token or expires_in:
	            cache.set(token_cache_key,token,expires_in-60)
	        return token or ''

	def get_access_token(self):
	    payload = {'grant_type': 'client_credential','appid': self.appid,'secret': self.app_secret}
	    url = 'https://api.weixin.qq.com/cgi-bin/token'
	    r = requests.get(url, params=payload, verify=False)
	    if(r.status_code == requests.codes.ok):
	    	res = r.json()
	    	return res
	    else:
	    	return False
	def get_wxacode_unlimit(self,scene):
	    access_token = self.get_token()
	    url = 'http://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token='+access_token
	    payload = {'scene': scene,'width':430,'auto_color':False,"line_color":{"r":"0","g":"0","b":"0"}}
	    r = requests.post(url, json = payload)
	    print(r.status_code)
	    #print(r.json())
	    return r.content    	       	

if __name__ == '__main__':
    app_id = os.environ["WXA_APP_ID"]
    app_secret = os.environ["WXA_APP_SECRET"] 
    wx = weixin(app_id,app_secret)     
    token = wx.get_wxacode_unlimit();                  
    print (token) 