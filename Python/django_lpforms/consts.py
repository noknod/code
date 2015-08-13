# -*- coding: utf-8 -*- 

FIELD_CHAR_MAXLENGTH = 200

VALUE_DOMEN_MAXLENGTH = 75
VALUE_REQUIRED_DEFAULT = False

import re

RE_VALID_DOMAIN = re.compile(
           r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$')

DB_TABLE_PREFIX = 'lpforms.public.'

ADMIN_DOMAINFORM_EXTRA = 3


from django.conf import settings

DB_POSTGRESQL, DB_SQLITE = ('postgresql_psycopg2', 'sqlite3')
DB_USING = settings.DATABASES['default']['ENGINE'].lower().split('.')[-1]

VALUE_SIMPLE_SHOWLEN = 25


FIELD_TYPES = (
    ('IR', 'Integer'),
    ('CR', 'Char'),
    ('TT', 'Text'),
)


VALUE_TEMPLATE_MAXLENGTH = 255


from os import path

TEMPLATE_DIR = path.join(path.dirname(path.realpath(__file__)), 'templates')
TEMPLATE_FILE = 'lpform.html'

SQL_SEARCH_DOMAIN = 'domain_id in (select itd.id from lpforms_domain itd ' + \
                    'where itd.domain like %s)'