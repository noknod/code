#from django.test import TestCase

# Create your tests here.




#from utils import fio_clean

from utils import fio_clean

d = 'КлюшкИн  23юрий '

print('"' + fio_clean(d) + '"')


###

import datetime

now_date = datetime.date.today()

print(now_date)

print(now_date.strftime("%d.%m.%Y")) 

now_date = now_date.replace(2011,6,1)
print(now_date.strftime("%d.%m.%Y")) 