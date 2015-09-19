# -*- coding: utf-8 -*-


import json

import scrapy
from scrapy.crawler import CrawlerProcess


from realty.spiders.realty import RealtySpider


from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())


"""
j = json.dumps({
  "project": "IRR.RU",
  "scrapy": {
    "concurrent_spiders": 10,
    "download_timeout": 15
  },
  "config": {
    "allowed_domains": [
      "irr.ru"
    ],
    "start_urls": [
      "http://irr.ru/real-estate/commercial/search/currency=RUR/sourcefrom=1/date_create=yesterday/",
    ],
    "link_extractors": {
      "follow_link": [
        u"/page\\d/$"
      ],
      "parse_link": [
        {u"method": u"re",
         u"/real-estate/.+/.+advert\\d+\\.html",
         u"prefix": u"http://irr.ru"}
      ]
    },
    "item": {
      "title": {
          "extractor": u"<h1>(.*?)</h1>"
      },
      "id": {
        "extractor": u"advertId\\s+=\\s+(\\d+);"
      }
    }
  },
  "params": {
    "separator": u'/',
    "params": [u'page_len60']
  },
  "limit": {
    "records": config.read("defaults.limit.records")
    }
})
project = json.loads(j)
"""

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

project = projects.get(project_code, code)
project[u'params'] = {}
project[u'limit'] = config.read("defaults.limit")

process.crawl(RealtySpider, project=project)
process.start() # the script will block here until the crawling is finished