# coding: utf-8

from django.core.wsgi import get_wsgi_application
from leancloud import Engine
from leancloud import LeanEngineError
from leancloud import Object
from leancloud import Query

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

