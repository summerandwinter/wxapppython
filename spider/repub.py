# coding: utf-8
#!/usr/bin/python3

import pymysql
import sys  
from leancloud import Object
from leancloud import Query
import leancloud

class Card(Object):
    pass

APP_ID = '7C7MfP24LboNSLeOnbh112nT-gzGzoHsz'
MASTER_KEY = 'bIEoNy5pSWoqvC3qq0vpGMT1'

leancloud.init(APP_ID, master_key=MASTER_KEY)

query = Card.query
query.does_not_exist('publishAt')
query.exists('user')
query.limit(1000)
cards = query.find()

for card in cards:
    _card = Card.create_without_data(card.id)
    _card.set('publishAt',card.get('updateAt'))
    _card.save()  
  
