# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
'''
class TycPipeline(object):
    # def process_item(self, item, spider):
        # return item
    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()'''
from pymongo import MongoClient  
from scrapy.conf import settings  
  
class TycPipeline(object):  
    def __init__(self):  
        connection = MongoClient(  
           settings[ 'MONGODB_SERVER' ],  
           settings[ 'MONGODB_PORT' ]  
        )  
        db = connection[settings[ 'MONGODB_DB' ]]  
        self.collection = db[settings[ 'MONGODB_COLLECTION' ]]  

    def process_item(self, item, spider):  
        postItem = dict(item)
        self.collection.insert(postItem)
        return item