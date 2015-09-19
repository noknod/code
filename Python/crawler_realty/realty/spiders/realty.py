# -*- coding: utf-8 -*- 


import re
import scrapy

from scrapy.selector import Selector


#from realty.consts import *
from ..items import RealtyItem
#from realty.items import RealtyItem
#from realty.loaders import RealtyProjectLoader



class RealtySpider(scrapy.Spider):

    name = "realty"

    def __init__(self, project, *args, **kwargs):
        super(RealtySpider, self).__init__(*args, **kwargs)

        self.allowed_domains = project[u'config'][u'allowed_domains']

        self.start_urls = self._get_start_urls(project)

        self.config = {
            #u"concurrent_spiders": project[u"scrapy"][u"concurrent_spiders"],
            #u"download_timeout": project[u"scrapy"][u"download_timeout"],
            u"follow_link": 
                        project[u"config"][u"link_extractors"][u"follow_link"],
            u"item": project[u"config"][u"item"],
            u"limit_items": project[u"limit"][u"records"], 
        }

        self.config[u"re_links"] = []
        for link in project[u"config"][u"link_extractors"][u"parse_link"]:
            print link
            if link[u'method'] == u're':
                self.config[u"re_links"].append({
                        u"link": re.compile(link[u'link'], re.UNICODE), 
                        u"prefix": link[u'prefix']
                    })

        #self.rules = self._get_rules(project)

        self._items_cnt = 0

        #print '\n#spider\n', self.allowed_domains, '\n'
        #print self.start_urls, '\n'
        #print self.config


    def parse(self, response):
        """  """
        for link in self._grab_links(response):
            #print link
            if self.check_item_maxcnt_reached():
                #print '\n#######\n######\nmax cnt\n' + str(self._items_cnt) + '\n'
                break
            yield scrapy.Request(self._get_realty_url(link), 
                    callback=self.parse_realty_page)
            self.inc_item_cnt()

        for page in self._get_next_page(response):
            #if self._current_page > self._pages and self._pages > 0:
            #    pages = self._grab_cnt_page(response)
            #    if pages > self._pages:
            #        self._pages = pages
            #if self._current_page < self._pages:
            #   yield scrapy.Request(self._get_next_page_url(
            #                      self._current_page + 1), callback=self.parse)
            yield scrapy.Request(page, callback=self.parse)


    def parse_realty_page(self, response):
        """
        l = CianProjectLoader(item=CianProjectItem(), response=response)
        l.add_value('url', unicode(response.url))
        for key, value in XPATHS_REALTY:
            l.add_xpath(key, value)
        return l.load_item()
        """

    """
    def _unimodify_arg(self, arg, types, name):
        if arg is None:
            return types[0]
        arg = unicode(arg).lower()
        if arg not in types:
            raise Exception(name + u' "' + arg + u'" is not supported!')
        return arg
    """


    def check_item_maxcnt_reached(self):
        """ Возвращает, достигнуто ли ограничение по числу информации """

        if self.config[u"limit_items"] == 0:
            return False

        return self._items_cnt >= self.config[u"limit_items"]


    def inc_item_cnt(self):
        """ Добавляет 1 к числу информации """

        self._items_cnt += 1


    def _get_start_urls(self, project):
        """ Возвращает список начальных ссылок из project """

        def _get_parametrized_url(self, url, params):
            """ Возвращает url с добавленными параметрами из params """

            sep = params[u'separator']
            params = params[u'params']
            part_url_with_params = sep.join(params)

            if sep == u'/':
                if url.endswith('/'):
                    return url + part_url_with_params + u'/'
                else:
                    return url + u'/' + part_url_with_params + u'/'

            elif sep == u'&':
                if url.find(sep) == -1:
                    return url + u'?' + part_url_with_params
                else:
                    return url + sep + part_url_with_params

        start_urls = project[u'config'][u'start_urls']
         
        params = project.get(u'params', None)
        if params:
            for index in xrange(0, len(start_urls)):
                start_urls[index] = self._get_parametrized_url(
                        start_urls[index], params)

        return start_urls
    """
    def _get_rules(self, project):
        rules = []
         (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )
    """

    def _get_next_page(self, response):
        print '\n#######\n######\n' + str(self.config[u'follow_link']) + '\n\n'
        if self.check_item_maxcnt_reached():
            return []
        #return self.start_urls[0] + u'&p=%d' % page

        print self.conf[u'follow_link']
        return []


    def _get_realty_url(self, link):
        return link#u'http://www.' + self.allowed_domains[0] + link

    """
    def _grab_cnt_page(self, response):
        sel = Selector(response)
        pages = sel.xpath(u'//div[@class="pager_pages"]')
        cnt_page = self._pages
        for page in pages.xpath(u'a/text()')[-2:]:
            text = page.extract().strip()
            if text.isdigit():
                dummy_page = int(text)
                if dummy_page > cnt_page:
                    cnt_page = dummy_page
        return cnt_page
    """

    def _grab_links(self, response):
        for re_link in self.config[u"re_links"]:
            for link in re_link[u'link'].findall(response.body):
                if re_link[u'prefix'] != u'':
                    yield re_link[u'prefix'] + link
                else:
                    yield link
        """
        #sel = Selector(response)
        links = sel.xpath(s)
        for link in links:
                yield link.extract()
        """


"""
{
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
      "http://irr.ru/real-estate/commercial/search/currency=RUR/sourcefrom=0/date_create=yesterday/page_len60/",
      "http://irr.ru/real-estate/commercial/search/currency=RUR/sourcefrom=1/date_create=yesterday/page_len60/",
      "http://irr.ru/real-estate/commercial-sale/search/currency=RUR/sourcefrom=0/date_create=yesterday/page_len60/",
      "http://irr.ru/real-estate/commercial-sale/search/currency=RUR/sourcefrom=1/date_create=yesterday/page_len60/"
    ],
    "link_extractors": {
      "follow_link": [
        "/page\\d/$"
      ],
      "parse_link": [
        "/real-estate/.+/.+advert\\d+\\.html$"
      ]
    },
    "item": {
      "title": {
          "extractor": "<h1>(.*?)</h1>"
      },
      "id": {
        "extractor": "advertId\\s+=\\s+(\\d+);"
      }
    }
  }
}
"""