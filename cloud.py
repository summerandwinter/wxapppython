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
import requests

engine = Engine(get_wsgi_application())

class Like(Object):
    pass
class Card(Object):
    pass  
class User(Object):
    pass
class _File(Object):
    pass
class Share(Object):
    pass
class Download(Object):
    pass
class View(Object):
    pass

def timebefore(d):  
    chunks = (  
                       (60 * 60 * 24 * 365, u'年'),  
                       (60 * 60 * 24 * 30, u'月'),  
                       (60 * 60 * 24 * 7, u'周'),  
                       (60 * 60 * 24, u'天'),  
                       (60 * 60, u'小时'),  
                       (60, u'分钟'),  
     )  
    #如果不是datetime类型转换后与datetime比较
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year,d.month,d.day)
    now = datetime.datetime.now()
    delta = now - d
    #忽略毫秒
    before = delta.days * 24 * 60 * 60 + delta.seconds
    #刚刚过去的1分钟
    if before <= 60:
        return '刚刚'
    if(d.year != now.year):
        return '%s年%s月%s日'%(d.year,d.month,d.day)
    if(before > 60 * 60 * 24 * 7):
        return '%s月%s日'%(d.month,d.day) 
    for seconds,unit in chunks:
        count = before // seconds
        if count != 0:
            break
    return str(count)+unit+"前"

def query_work(uid,page):
    pageSize = 10  
    skip = (page-1)*pageSize
    user = User.create_without_data(uid)
    query = Card.query
    query.add_descending('createdAt')
    query.equal_to('user',user)
    count = query.count()
    query.limit(10)
    query.skip(skip)
    cards = query.find()
    ret = {}
    ret['code'] = 200
    dataList = []
    for card in cards:
        data = {}
        data['id'] = card.id
        data['name'] = card.get('name')
        data['content'] = card.get('content')
        data['img_url'] = card.get('img_url')
        data['shares'] = card.get('shares')
        data['likes'] = card.get('likes')
        data['time'] = timebefore(card.get('createdAt').replace(tzinfo=None))
        dataList.append(data)
    ret['count'] = count
    ret['hasMore'] = count > (page*pageSize) 
    ret['page'] = page    
    ret['data'] = dataList
    return ret

@engine.define
def hello(**params):
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.define
def explore(**params):
    page = 1
    if 'page' in params:
        page = params['page']
    pageSize = 10  
    skip = (page-1)*pageSize
    query = Card.query
    query.include('user')
    query.equal_to('publish', True)
    query.add_descending('createdAt')
    count = query.count()
    query.limit(10)
    query.skip(skip)
    cards = query.find()
    ret = {}
    ret['code'] = 200
    dataList = []
    for card in cards:
        data = {}
        data['id'] = card.id
        data['name'] = card.get('name')
        data['content'] = card.get('content')
        data['img_url'] = card.get('img_url')
        data['shares'] = card.get('shares')
        data['likes'] = card.get('likes')
        print(card.get('createdAt'))
        data['time'] = timebefore(card.get('createdAt').replace(tzinfo=None))
        user = {}
        _user = card.get('user')
        user['id'] = _user.id
        user['nickName'] = _user.get('nickName')
        user['avatarUrl'] = _user.get('avatarUrl')
        user['gender'] = _user.get('gender')
        user['city'] = _user.get('city')
        user['province'] = _user.get('province')
        data['user'] = user
        dataList.append(data)
    ret['count'] = count
    ret['hasMore'] = count > (page*pageSize) 
    ret['page'] = page    
    ret['data'] = dataList
    return ret

@engine.define
def selection(**params):
    page = 1
    if 'page' in params:
        page = params['page']
    pageSize = 10  
    skip = (page-1)*pageSize
    query = Card.query
    query.include('user')
    query.equal_to('publish', True)
    query.add_descending('likes')
    count = query.count()
    query.limit(10)
    query.skip(skip)
    cards = query.find()
    ret = {}
    ret['code'] = 200
    dataList = []
    for card in cards:
        data = {}
        data['id'] = card.id
        data['name'] = card.get('name')
        data['content'] = card.get('content')
        data['img_url'] = card.get('img_url')
        data['shares'] = card.get('shares')
        data['likes'] = card.get('likes')
        print(card.get('createdAt'))
        data['time'] = timebefore(card.get('createdAt').replace(tzinfo=None))
        user = {}
        _user = card.get('user')
        user['id'] = _user.id
        user['nickName'] = _user.get('nickName')
        user['avatarUrl'] = _user.get('avatarUrl')
        user['gender'] = _user.get('gender')
        user['city'] = _user.get('city')
        user['province'] = _user.get('province')
        data['user'] = user
        dataList.append(data)
    ret['count'] = count
    ret['hasMore'] = count > (page*pageSize) 
    ret['page'] = page    
    ret['data'] = dataList
    return ret

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
    if 'formId' in params:
        formId = params['formId']
        card.set('formId',formId)
    image = _File.create_without_data(file)
    if 'userid' not in params:
        query = User.query
        query.equal_to('username',username)
        user = query.first()
        card.set('user',user)
    else:
        userid = params['userid']
        user = User.create_without_data(userid)
        card.set('user',user)       
    card.set('user',user)
    card.set('image',image)
    card.set('publish',False)
    card.set('likes',0)
    card.set('shares',0)
    card.save()
    stat = generateCloud(card)
    if stat == 'ok':
    	result = {'code':200,'data':card.get('objectId')}
    	return result
    else:
    	result = {'code':500,'message':'failed'}
    	return result
    
@engine.define
def profile(**params):
    uid = params['id']
    likequery = Like.query
    user = User.create_without_data(uid)
    likequery.equal_to('user',user)
    like_count = likequery.count()
    workquery = Card.query
    workquery.equal_to('user',user)
    work_count = workquery.count();
    count = {}
    count['likes'] = like_count
    count['works'] = work_count
    page = 1
    data = query_work(uid,page)
    result = {'code':200,'count':count,'works':data}
    return result

@engine.define
def isLiked(**params):
    if 'id' not in params:
        return False
    if 'uid' not in params:
        return False
    id = params['id']
    uid = params['uid']
    user = User.create_without_data(uid)
    card = Card.create_without_data(id)
    query = Like.query
    query.equal_to('user',user)
    query.equal_to('card',user)
    count = query.count()
    return count>0


        

@engine.define
def detail(**params):
    try:
        id = params['id']
        query = Card.query
        query.include('photo')
        query.include('user')
        card = query.get(id)
        data = {}
        data['id'] = card.id
        data['name'] = card.get('name')
        data['content'] = card.get('content')
        data['img_url'] = card.get('img_url')
        data['shares'] = card.get('shares')
        data['likes'] = card.get('likes')
        data['time'] = timebefore(card.get('createdAt').replace(tzinfo=None))
        user = {}
        _user = card.get('user')
        user['id'] = _user.id
        user['nickName'] = _user.get('nickName')
        user['avatarUrl'] = _user.get('avatarUrl')
        user['gender'] = _user.get('gender')
        user['city'] = _user.get('city')
        user['province'] = _user.get('province')
        data['user'] = user
        photo = card.get('photo');
        data['preview'] = photo.get('url')
        data['download'] = 'https://timesand.leanapp.cn/card/download/'+id+'.png'
        isliked = False
        if 'uid' in params:
            uid = params['uid']
            likequery = Like.query
            likequery.equal_to('card',card)
            user = User.create_without_data(uid)
            likequery.equal_to('user',user)
            count = likequery.count()
            if count >0 :
                isliked = True
        data['isLiked'] = isliked
        result = {'code':200,'data':data}
        return result
    except LeanCloudError as e:
        result = {'code':e.code,'message':e.error}
        return result

@engine.define
def works(**params):
    uid = params['id']
    page = 1
    if 'page' in params:
        page = params['page']
    return query_work(uid,page)

@engine.define
def likes(**params):
    uid = params['id']
    page = 1
    if 'page' in params:
        page = params['page']
    pageSize = 10  
    skip = (page-1)*pageSize
    user = User.create_without_data(uid)
    query = Like.query
    query.include('card')
    query.include('user')
    query.equal_to('user', user)
    query.add_descending('createdAt')
    count = query.count()
    query.limit(10)
    query.skip(skip)
    likes = query.find()
    ret = {}
    ret['code'] = 200
    dataList = []
    for like in likes:
        data = {}
        card = like.get('card')
        data['id'] = card.id
        data['name'] = card.get('name')
        data['content'] = card.get('content')
        data['img_url'] = card.get('img_url')
        data['shares'] = card.get('shares')
        data['likes'] = card.get('likes')
        data['time'] = timebefore(card.get('createdAt').replace(tzinfo=None))
        user = {}
        _user = like.get('user')
        user['id'] = _user.id
        user['nickName'] = _user.get('nickName')
        user['avatarUrl'] = _user.get('avatarUrl')
        user['gender'] = _user.get('gender')
        user['city'] = _user.get('city')
        user['province'] = _user.get('province')
        data['user'] = user
        dataList.append(data)
    ret['count'] = count
    ret['hasMore'] = count > (page*pageSize) 
    ret['page'] = page    
    ret['data'] = dataList
    return ret
    
@engine.define
def templates(**params):
    data = [
        {'id':1,'url':'http://7rfkul.com1.z0.glb.clouddn.com/template.png'},
        {'id':2,'url':'http://7rfkul.com1.z0.glb.clouddn.com/template2.png'},
        {'id':3,'url':'http://7rfkul.com1.z0.glb.clouddn.com/template3.png'},
        {'id':4,'url':'http://7rfkul.com1.z0.glb.clouddn.com/template4.png'}
    ]
    result = {'code':200,'data':data}
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


@engine.define
def share(**params):
    try:
        if 'id' not in params:
            return {'code':301,'message':'参数错误'}
        share = Share()
        id = params['id']
        card = Card.create_without_data(id)
        share.set('card',card)
        if 'uid' in params:
            uid = params['uid']
            user =  User.create_without_data(uid)
            share.set('user',user)
        if 'tickets' in params:
            tickets = params['tickets']
            share.set('tickets',tickets)
        share.save()
        card.increment('shares')
        card.fetch_when_save = True
        card.save()
        return {'code':200,'message':'ok'}
    except LeanCloudError as e:
        print(e)
        result = {'code':e.code,'message':e.error}
        return result

@engine.define
def download(**params):
    try:
        if 'id' not in params:
            return {'code':301,'message':'参数错误'}
        download = Download()
        id = params['id']
        card = Card.create_without_data(id)
        download.set('card',card)
        if 'uid' in params:
            uid = params['uid']
            user =  User.create_without_data(uid)
            download.set('user',user)
        download.save()
        card.increment('downloads')
        card.fetch_when_save = True
        card.save()
        return {'code':200,'message':'ok'}
    except LeanCloudError as e:
        print(e)
        result = {'code':e.code,'message':e.error}
        return result

@engine.define
def view(**params):
    try:
        if 'id' not in params:
            return {'code':301,'message':'参数错误'}
        view = View()
        id = params['id']
        card = Card.create_without_data(id)
        view.set('card',card)
        if 'uid' in params:
            uid = params['uid']
            user =  User.create_without_data(uid)
            view.set('user',user)
        view.save()
        card.increment('views')
        card.fetch_when_save = True
        card.save()
        return {'code':200,'message':'ok'}
    except LeanCloudError as e:
        print(e)
        result = {'code':e.code,'message':e.error}
        return result

@engine.define
def movies(**params):
    id = params['id']
    payload = {}
    url = 'http://api.markapp.cn/v160/Mobile/movies/'+id
    r = requests.get(url, params=payload, verify=False)
    if(r.status_code == requests.codes.ok):
        res = r.json()
        return res
    else:
        return {'status':0,'message':'error'}    

@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')

