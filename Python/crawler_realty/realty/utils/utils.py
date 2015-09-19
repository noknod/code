# -*- coding: utf-8 -*-


import re


from realty.consts import RE_CODE_CLEANER, RE_ONLY_ONE_SPACE



def code_clean(code):
    """ Возвращает очищенный код """
    code = RE_ONLY_ONE_SPACE.sub(u' ', 
            RE_CODE_CLEANER.sub(u'', code.lower()))
    return code.strip()



"""
RE_RMV_M2 = re.compile(ur'>\s*([\s\w\.\(\)-]*)(?!</s)', re.UNICODE)

RE_SUB_WS = re.compile(ur'\s+', re.UNICODE)


RE_TOTAL_SQUARE_FLAT = re.compile(ur'</i>(\d+)', re.UNICODE)
RE_TOTAL_SQUARE_OFFICE = re.compile(ur'<td>\s*(\d+)\s*м', re.UNICODE)
RE_TOTAL_SQUARE_SUBURBAN = re.compile(ur'<td>\s*(\d+)\s*с', re.UNICODE)



def remove_ws(txt):
    return RE_SUB_WS.sub(u' ', txt).strip()


def remove_m2(txt):
    data = RE_RMV_M2.findall(txt)
    return u' '.join(word.strip() for word in data if word.strip() != u'')
"""