# -*- coding: utf-8 -*-



import scrapy

from scrapy.selector import Selector


from cian_project.const import *
from cian_project.items import CianProjectItem
from cian_project.loaders import CianProjectLoader



class CianSpider(scrapy.Spider):
    name = "cian"
    allowed_domains = ["cian.ru"]


    def __init__(self, deal_type=None, realty=None, region=None, params=None,
                 *args, **kwargs):
        super(CianSpider, self).__init__(*args, **kwargs)

        self._deal_type = self._unimodify_arg(deal_type, DEAL_TYPES, 
                                              u'Deal type')
        self._realty = self._unimodify_arg(realty, REALTY_TYPES, 
                                           u'Realty type')
        self._region = START_URI_PART_REGION if region is None else region
        self._params = params
        self.start_urls = [self._get_start_url()]

        self._pages = 0
        self._current_page = 0
        self._items = 0

        if GRAB_CNT_PAGE_MIN > 0 and GRAB_CNT_ITEM_MIN > 0:
            self._is_done = self._is_done_all
        elif GRAB_CNT_PAGE_MIN > 0:
            self._is_done = self._is_done_by_pages
        elif GRAB_CNT_ITEM_MIN > 0:
            self._is_done = self._is_done_by_items
        else:
            self._is_done = self._is_done_false


    def parse(self, response):
        if self._pages == 0:
            self._pages = self._grab_cnt_page(response)
        self._current_page += 1
        for link in self._grab_links(response):
            yield scrapy.Request(self._get_realty_url(link), 
                                 callback=self.parse_realty_page)
            self._items += 1
            if self._is_done():
                break
        if not self._is_done():
            if self._current_page > self._pages and self._pages > 0:
                pages = self._grab_cnt_page(response)
                if pages > self._pages:
                    self._pages = pages
            if self._current_page < self._pages:
               yield scrapy.Request(self._get_next_page_url(
                                  self._current_page + 1), callback=self.parse)


    def parse_realty_page(self, response):
        l = CianProjectLoader(item=CianProjectItem(), response=response)
        l.add_value('url', unicode(response.url))
        for key, value in XPATHS_REALTY:
            l.add_xpath(key, value)
        return l.load_item()


    def _unimodify_arg(self, arg, types, name):
        if arg is None:
            return types[0]
        arg = unicode(arg).lower()
        if arg not in types:
            raise Exception(name + u' "' + arg + u'" is not supported!')
        return arg


    def _is_done_by_items(self):
        return self._items >= GRAB_CNT_ITEM_MIN

    def _is_done_by_pages(self):
        return self._current_page > GRAB_CNT_PAGE_MIN

    def _is_done_false(self):
        return False

    def _is_done_all(self):
        return (self._items >= GRAB_CNT_ITEM_MIN and 
                self._current_page >= GRAB_CNT_PAGE_MIN)


    def _get_start_url(self):
        if self._params is None:
            params = (START_URI % (self._deal_type, self._realty), 
                      self._region)
        else:
            params = (START_URI % (self._deal_type, self._realty), 
                      self._region, self._params)
        return u'&'.join(params)


    def _get_next_page_url(self, page):
        return self.start_urls[0] + u'&p=%d' % page


    def _get_realty_url(self, link):
        return REALTY_PART_URI % link


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


    def _grab_links(self, response):
        sel = Selector(response)
        links = sel.xpath(XPATHS_LINK[self._realty])
        for link in links:
            yield link.extract()