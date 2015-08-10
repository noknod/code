# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html



import scrapy



class CianProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rent_type = scrapy.Field()
    url = scrapy.Field()
    total_square = scrapy.Field()
    cost = scrapy.Field()
    address = scrapy.Field()
    info = scrapy.Field()
    phones = scrapy.Field()