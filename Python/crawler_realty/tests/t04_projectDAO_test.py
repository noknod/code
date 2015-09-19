# -*- coding: utf-8 -*- 


from realty.config.config import Config
from realty.utils import errorhandler
from realty.models.db import get_database
from realty.models.projectDAO import ProjectDAO


error_handler = errorhandler.get_error_handler()

config = Config(error_handler)

database = get_database(config)

projects = ProjectDAO(database, error_handler)


project_code = u'irr.ru'
code = u'general'
scrapy_config = {
    u"concurrent_spiders": 10,
    u"download_timeout": 15
  }
project_config = {
    u"allowed_domains": [
        u"irr.ru"
    ],
    u"start_urls": [
        u"http://irr.ru/real-estate/commercial/search/currency=RUR/sourcefrom=0/date_create=yesterday/page_len60/",
        u"http://irr.ru/real-estate/commercial/search/currency=RUR/sourcefrom=1/date_create=yesterday/page_len60/",
        u"http://irr.ru/real-estate/commercial-sale/search/currency=RUR/sourcefrom=0/date_create=yesterday/page_len60/",
        u"http://irr.ru/real-estate/commercial-sale/search/currency=RUR/sourcefrom=1/date_create=yesterday/page_len60/"
    ],
    u"link_extractors": {
        u"follow_link": [
            u"/page\\d/$"
        ],
        u"parse_link": [
            {
                u"link": u"/real-estate/.+/.+advert\\d+\\.html",
                u"method": u"re",
                u"prefix": u"http://irr.ru"
            }
        ]
    },
    u"item": {
        u"title": {
            u"extractor": u"<h1>(.*?)</h1>"
      },
      u"id": {
            u"extractor": u"advertId\\s+=\\s+(\\d+);"
      }
    },
  }
info = u'Сайт www.irr.ru: основной поиск'

print '*project_code, code\n', projects.get(project_code, code), u'\n'

"""
uris = {"start": u'http://www.cian.ru/cat.php?deal_type=rent&flats=yes', 
        "part":  u'http://www.cian.ru%s',
        "next": u'//div[@class="object_actions"]/a/@href'}

info = [
    ('rent_type', u'//div[@class="object_descr_title"]'), 

    ('total_square', u'//table[@class="object_descr_props"]'),
    ('total_square', u'//table[@class="object_descr_props"]/tr'),

    ('cost', u'//div[@class="object_descr_price"]/text()'),

    ('address', u'//h1[@class="object_descr_addr"]/text()'),

    ('info', u'//div[@class="object_descr_text"]'),

    ('phones', u'//strong[@class="object_descr_phone_orig"]/a/text()')
]
"""

project = projects.upsert_project(project_code, code, scrapy_config, project_config, info)
print '*upsert return\n', project

print '\n*project_code, code\n', projects.get(project_code, code), u'\n'

print u'\n', projects.get_by_id(project[u'_id'])

params = {u"code": u"simple", u"separator": u"/", u"params": [u"params"]}

project = projects.push_params(project_code, code, params)

print u'\n*push return\n', project.modified_count

d = list(projects.filter())
print u'\n*filter return\n', d