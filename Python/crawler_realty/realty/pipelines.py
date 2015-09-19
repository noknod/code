# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem



class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()


    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            raise DropItem(u'Обнаружен дупликат: %s' % item)
        else:
            self.ids_seen.add(item['id'])
            return item



class ValidationPipeline(object):

    def process_item(self, item, spider):
        
        if spider.check_item_maxcnt_reached:
            spider.log(u'Достигнут предел информации.', log.INFO)
            raise DropItem()
        
        spider.inc_item_cnt()

        return item


"""
class MongoPipeline(object):

    def __init__(self, infoDAO):
        self.infoDAO = infoDAO


    def process_item(self, item, spider):
        self.infoDAO.push_item((dict(item))
        return item
"""