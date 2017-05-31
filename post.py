import sys  
import http.client
import urllib
import urllib.request
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
	token = get_access_token();
	access_token = token['access_token']
	conn = http.client.HTTPConnection("api.weixin.qq.com")
	data = {'scene': '1234567898','width':430,'auto_color':False,"line_color":{"r":"0","g":"0","b":"0"}}
	payload = "{\"scene\": \"1234567898\",\"width\":430,\"auto_color\":false,\"line_color\":{\"r\":\"0\",\"g\":\"0\",\"b\":\"0\"}}"
	headers = {'content-type': "application/json",'cache-control': "no-cache"}
	conn.request("POST", "/wxa/getwxacodeunlimit?access_token="+access_token, payload, headers)
	res = conn.getresponse()
	data = res.read()print(data.decode("utf-8"))
  

