import django

django.setup()


import lpforms.models

md = lpforms.models.Domain
mf = lpforms.models.DomainForm
ms = lpforms.models.FormPostSeq
mfs = lpforms.models.FormSimple
mft = lpforms.models.FormText

domain_name = 'www.yandex.ru'
f1_name = 'f1'
f2_name = 'f2'
f3_name = 'f3'
"""
domain = md.objects.create(domain=domain_name)
domain.save()

f1 = mf.objects.create(domain_id=domain.id, fname=f1_name, ftype='IR')
f1.save()
f2 = mf.objects.create(domain_id=domain.id, fname=f2_name, ftype='CR', length=15)
f2.save()
f3 = mf.objects.create(domain_id=domain.id, fname=f3_name, ftype='TT')
f3.save()
"""

import lpforms.utils
c = lpforms.utils.MessagePostManager
o = c(md, mf, ms, mfs, mft)

message = {f1_name: 12, f2_name: 'char text', f3_name: 'full text'}
o.post(domain_name, message)
o.post(domain_name, message)

print('done')
"""
domain_id = o._get_domain_id(domain)

message = {'f1': '12', 'f2': 'asdf', 'f3': 'full text'}

message2 = {'f1': '12', 'f23': 'asdf', 'f3': 'full text'}
fields = o._read_fields(domain_id, message2)

'Поле формы "{0}" для доменного имени "{1}" ' + 'не задано!'.format(domain, fields[1])

 message_id = lpforms.utils.get_nextval_from_sequence(ms)

o._do_post(message_id, fields[1:])
"""