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
from card import *

engine = Engine(get_wsgi_application())

class Like(Object):
    pass
class Card(Object):
    pass  
class User(Object):
    pass
class _File(Object):
    pass           

@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'

@engine.define
def maker(**params):
    name = params['name']
    content = params['content']
    file = params['file']
    img_url = params['img_url']
    username = params['username']
    template = params['template']
    card = Card()
    card.set('name',name)
    card.set('content',content)
    card.set('img_url',img_url)
    card.set('username',username)
    card.set('template',template)
    image = _File.create_without_data(file)
    card.set('image',image)
    card.save()
    stat = generateCloud(card)
    if stat == 'ok':
    	result = {'code':200,'data':card.get('objectId')}
    	return result
    else:
    	result = {'code':500,'message':'failed'}
    	return result
    


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

