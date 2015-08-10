# -*- coding: utf-8 -*- 

FIELD_CHAR_MAXLENGTH = 200

VALUE_DOMEN_MAXLENGTH = 75
VALUE_REQUIRED_DEFAULT = False

import re

RE_VALID_DOMAIN = re.compile(
           r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$')

DB_TABLE_PREFIX = 'lpforms.public.'

ADMIN_DOMAINFORM_EXTRA = 3

DB_USES = 'SQLite'
#DB_USES = 'PostgreSQL'