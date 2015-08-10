# -*- coding: utf-8 -*-



import re


from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose, TakeFirst, Join


from cian_project.utils import remove_ws, remove_m2



RE_TOTAL_SQUARE_FLAT = re.compile(ur'</i>(\d+)', re.UNICODE)
RE_TOTAL_SQUARE_OFFICE = re.compile(ur'<td>\s*(\d+)\s*м', re.UNICODE)
RE_TOTAL_SQUARE_SUBURBAN = re.compile(ur'<td>\s*(\d+)\s*с', re.UNICODE)


RE_INFO_AGENT = re.compile(
    ur'><br>\s*([\w\W]+)\s*<div class="object_descr_phones">', re.UNICODE)
RE_INFO = re.compile(
    ur'text">\s*([\w\W]+)\s*<div class="object_descr_phones">', re.UNICODE)
AGENT_INFO = (u'По какой-то причине этот агент не готов сотрудничать' +  
             u'с другими агентами.\n\n')



def get_total_square(txt):
    total_suare = None
    if u'Общая площадь' in txt:
        total_suare = RE_TOTAL_SQUARE_FLAT.findall(txt)[0]
    elif u'Площадь:' in txt:
        total_suare = RE_TOTAL_SQUARE_OFFICE.findall(txt)[0]
    elif u'Площадь участка:' in txt:
        total_suare = RE_TOTAL_SQUARE_SUBURBAN.findall(txt)[0]
    return total_suare


def get_info(txt):
    if u'Просьба агентам не звонить.' in txt:
        info = AGENT_INFO + RE_INFO_AGENT.findall(txt)[0]
    else:
        info = RE_INFO.findall(txt)[0]
    return info



class CianProjectLoader(ItemLoader):

    default_output_processor = TakeFirst()

    rent_type_in = MapCompose(remove_ws, remove_m2)

    total_square_in = MapCompose(get_total_square)

    cost_in = MapCompose(remove_ws)

    address_in = MapCompose(remove_ws)

    info_in = MapCompose(get_info, remove_ws)

    phones_in = MapCompose(remove_ws)
    phones_out = Join(u', ')