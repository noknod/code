# -*- coding: utf-8 -*-



import re



GRAB_CNT_PAGE_MIN = 2
GRAB_CNT_ITEM_MIN = 20


DEAL_TYPES = (u'rent', u'sale')
REALTY_TYPES = (u'flats', u'offices', u'suburbian')


IS_NEED_JSON = True


START_URI = u'http://www.cian.ru/cat.php?deal_type=%s&%s=yes'
START_URI_PART_REGION = u'obl_id=43&raion_obl_id[1]=347'

REALTY_PART_URI = u'http://www.cian.ru%s'


XPATHS_LINK = {
    u'suburbian' : 
    u'//a[@class="objects_item_info_col_card_link no-mobile"]/@href',

    u'offices' :
    u'//a[@class="objects_item_info_col_card_link no-mobile"]/@href', 

    u'flats' : 
    u'//div[@class="object_actions"]/a/@href'}

XPATHS_REALTY = [
    ('rent_type', u'//div[@class="object_descr_title"]'), 

    ('total_square', u'//table[@class="object_descr_props"]'),
    ('total_square', u'//table[@class="object_descr_props"]/tr'),

    ('cost', u'//div[@class="object_descr_price"]/text()'),

    ('address', u'//h1[@class="object_descr_addr"]/text()'),

    ('info', u'//div[@class="object_descr_text"]'),

    ('phones', u'//strong[@class="object_descr_phone_orig"]/a/text()')
]