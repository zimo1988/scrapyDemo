# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from spCollector import settings

class SpcollectorPipeline(object):
    def process_item(self, item, spider):
        return item


class SuseSolutionPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings.MONGO_HOST, port=settings.MONGO_PORT)
        # self.client.admin.authenticate(settings['MINGO_USER'], settings['MONGO_PSW'])
        self.db = self.client[settings.MONGO_DB]
        self.coll = self.db[settings.MONGO_COLL_SUSE_SOLUTION]

    def process_item(self, item, spider):
        if spider.name == 'suseSolution':
            dataSet = self.coll.find({'id': str(item['id'])})
            if dataSet.count() < 1:
                postItem = dict(item)
                self.coll.insert(postItem)
            return item

    def close_spider(self, spider):
        self.client.close()