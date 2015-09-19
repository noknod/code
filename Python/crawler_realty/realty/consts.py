# -*- coding: utf-8 -*- 


import re



# Регулярное выражение для очистки строки от символов, отличающихся от 
# букв, пробела, "_" и "."
RE_CODE_CLEANER = re.compile(ur'([^a-z _.])', re.UNICODE)

# Регулярное выражение для очистки строки от лишних пробелов
RE_ONLY_ONE_SPACE = re.compile(ur'(\s+)', re.UNICODE)