import http.client
import urllib
import json

def send_request(host, path, method, port=443, params={}):
    client = http.client.HTTPSConnection(host, port)
 
    path = '?'.join([path, urllib.parse.urlencode(params)])
    client.request(method, path)
 
    res = client.getresponse()
    if not res.status == 200:
        return False, res.status
 
    return True, json.loads(res.read().decode('utf-8'))



def get_access_token():
	app_id = 'wx68832af6b170b45f'
	app_secret = 'a17b0415c3bb1489e5129dfeacd470e9'
	params = {'grant_type': 'client_credential','appid': app_id,'secret': app_secret}
	host = 'api.weixin.qq.com'
	path = '/cgi-bin/token'
	method = 'GET'
	res = send_request(host, path, method, params=params)
	if not res[0]:
		log_error(res[1])
		return False
	if res[1].get('errcode'):
		log_error(res[1].get('errmsg'))
		return False
	return res[1]    
def getwxacodeunlimit():
	res = get_access_token()
	access_token = res['access_token']
	params = {'access_token': access_token}
	host = 'api.weixin.qq.com'
	path = '/wxa/getwxacodeunlimit'
	method = 'POST'
	res = send_request(host, path, method, params=params)
	if not res[0]:
		print(res[1])
		return False
	if res[1].get('errcode'):
		print(res[1].get('errmsg'))
		return False
	return res[1]   
res = getwxacodeunlimit()
print(res)    