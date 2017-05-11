# coding: utf-8

from django.core.wsgi import get_wsgi_application
from leancloud import Engine
from leancloud import LeanEngineError
from leancloud import Object
from leancloud import Query
from qiniu import Auth, set_default, etag, PersistentFop, build_op, op_save, Zone
from qiniu import put_data, put_file, put_stream
from qiniu import BucketManager, build_batch_copy, build_batch_rename, build_batch_move, build_batch_stat, build_batch_delete
from qiniu import urlsafe_base64_encode, urlsafe_base64_decode
from io import StringIO
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageFilter
from io import BytesIO
from textwrap import *

engine = Engine(get_wsgi_application())

class Like(Object):
    pass
class Card(Object):
    pass  
class User(Object):
    pass       

@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'

@engine.define
def like(**params):
    card_id = params['cid']
    user_id = params['uid']
    card = Card.create_without_data(card_id)
    user = User.create_without_data(user_id)
    query = Query(Like)
    query.equal_to('card', card)
    query.equal_to('user', user) 
    count = query.count() 
    if count == 0:
    	like = Like(card=card,user=user)
    	try:
    		like.save()
    		card.increment('likes')
    		card.fetch_when_save = True
    		card.save()
    		return 'ok'
    	except LeanCloudError as e:
        	return HttpResponseServerError(e.error)
    else:
    	return 'no'

@engine.define
def qiniu():
    #qiniu.conf.ACCESS_KEY = 'tyqeKgL8GqUmLsWKf1LVdg9RgCdgwKtRza9CEKDt'
    #qiniu.conf.SECRET_KEY = 'Zc-FxrpR6Y4pVzatmdL-Pw5eA49e-szFrUiNDsj4'
    #policy = qiniu.rs.PutPolicy('miposter') #bucket_name 就是那个你创建的空间的名字
    #uptoken = policy.token()
    #data=open('photo.jpg')
    #ret, err = qiniu.io.put(uptoken, None, data) #key直接none就可以
    #需要填写你的 Access Key 和 Secret Key
    url = 'oppyrwj3t.bkt.clouddn.com';
    access_key = 'tyqeKgL8GqUmLsWKf1LVdg9RgCdgwKtRza9CEKDt'
    secret_key = 'Zc-FxrpR6Y4pVzatmdL-Pw5eA49e-szFrUiNDsj4'
    #构建鉴权对象
    q = Auth(access_key, secret_key)
    #要上传的空间
    bucket_name = 'card'
    key = 'temp'
    data = BytesIO();
    template(data);
    token = q.upload_token(bucket_name)
    ret, info = put_data(token, key, data.getvalue())

    return ret	

def template(msstream):
    w = 640
    h = 862
    iw = 600
    ih = 340
    title = '每日一言'
    content = '觉得最失落的，大概是你还在为你们的未来出谋划策，他却已慢慢后退不再与你并肩。' 
    spacing = 20
    content = fill(content, 15)
    author = '- 拾光笔记 -' 
    copyright = '微信小程序「拾光笔记」'  
    title_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 35)
    content_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 30)
    author_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    copyright_fnt = ImageFont.truetype('font/zh/YueSong.ttf', 25)
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)
    tw,th = draw.multiline_textsize(title, font=title_fnt)
    aw,ah = draw.multiline_textsize(author, font=author_fnt)
    cw,ch = draw.multiline_textsize(content, font=content_fnt, spacing=spacing)
    crw,crh = draw.multiline_textsize(copyright, font=copyright_fnt)
    h = 635+th+ch+crh+ah;
    base = Image.new('RGBA',(w,h),(255,255,255,255))
    draw = ImageDraw.Draw(base)

    

    photo = Image.open("photo.jpg").convert('RGBA')

    (pw, ph) = photo.size
    if pw/ph>iw/ih:
        box = ((pw-ph*iw/ih)/2,0,(pw+ph*iw/ih)/2,ph)
    else:
        box = (0,(ph-pw*ih/iw)/2,pw,(ph+pw*ih/iw)/2)  

    photo = photo.crop(box)
    photo = photo.resize((iw,ih))
    base.paste(photo,box=(20,20))
    # get a drawing context
    draw = ImageDraw.Draw(base)
    # draw text in the middle of the image, half opacity
    draw.multiline_text((w/2-tw/2,420), title, font=title_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w/2-cw/2,420+th+45), content, font=content_fnt, fill=(0,0,0,255), align='center', spacing=spacing)
    draw.multiline_text((w/2-aw/2,420+th+45+ch+115), author, font=author_fnt, fill=(0,0,0,255), align='center')
    draw.multiline_text((w-crw,420+th+45+ch+115+ah+50), copyright, font=copyright_fnt, fill=(189,189,189,255), align='center')
   

    # save image data to output stream
    base.save(msstream,"png")
    # release memory
    base.close()
    return msstream

@engine.define
def cancel(**params):
    card_id = params['cid']
    user_id = params['uid']
    card = Card.create_without_data(card_id)
    user = User.create_without_data(user_id)
    query = Query(Like)
    query.equal_to('card', card)
    query.equal_to('user', user) 
    count = query.count() 
    
    if count >0 :
    	try:
    		likes = query.first()
    		likes.destroy()

    		card.increment('likes',-1)
    		card.fetch_when_save = True
    		card.save()
    		return 'ok'
    	except LeanCloudError as e:
        	return HttpResponseServerError(e.error)
    else:
    	return 'no'    



@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')

