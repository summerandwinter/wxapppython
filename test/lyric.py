import requests
import base64
import re
import json
from io import BytesIO

def loads_jsonp(_jsonp):
	try:
		return json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
	except:
		raise ValueError('Invalid Input')

def parse_lyric(_lyric):
	lyrics = _lyric.split('\n')
	_lyrics = []
	time_reg = '\[\d*:\d*((\.|\:)\d*)*\]'
	for line in lyrics:
		if re.match(time_reg,line,re.S) is not None:
		    newline = re.sub(time_reg,'',line,0)
		    if len(newline) > 0:
		    	_lyrics.append(newline)
	return _lyrics		   


def main():
    url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg"
    headers = {'referer': 'https://y.qq.com/portal/player.html','user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'}
    songmid = '001qrn6E3cqJih'
    payload = {'songmid':songmid,'pcachetime':'1497862380731','g_tk':'5381','oginUin':0,'hostUin':0,'format':'jsonp','inCharset':'utf8','outCharset':'utf-8','notice':0,'platform':'yqq','needNewCode':0}
    r = requests.get(url,params = payload,headers=headers)
    if(r.status_code == 200):
    	ret = loads_jsonp(r.text)
    	if(ret['code'] == 0):
    		lyric = base64.b64decode(ret['lyric']).decode('utf-8')
    		lyrics = parse_lyric(lyric)
    		print(lyrics)

if __name__ == "__main__":
    main()