# -*- coding: utf-8 -*- 


import re

from django.conf import settings



# Регулярное выражение для очистки строки от символов, отличающихся от 
# русских букв и пробела
RE_ONLY_ALPHA_AND_SPACE = re.compile(r'([^йцукенгшщзхъфывапролджэячсмитьбю ])')

# Регулярное выражение для очистки строки от лишних пробелов
RE_ONLY_ONE_SPACE = re.compile(r'(\s+)')



# Префикс для поиска таблиц при использовании PostgreSQL 
DB_TABLE_PREFIX = 'aclinic.public.'

# Обозначения движков баз данных при определении типа используемой базы
DB_POSTGRESQL, DB_SQLITE = ('postgresql_psycopg2', 'sqlite3')
# Определении типа используемой базы
DB_USING = settings.DATABASES['default']['ENGINE'].lower().split('.')[-1]



# Задаёт количество дней поиска вперёд свободных докторов
FIND_ADMISSION_DAYS_AHEAD = 15



# Пустое значение для невыбранного поля ChoiceField
BLANK_CHOICE = ('---', '--- Выберите значение ---',) 