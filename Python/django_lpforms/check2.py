import django

django.setup()


import lpforms.models

md = lpforms.models.Domain
mf = lpforms.models.DomainForm
ms = lpforms.models.FormPostSeq
mfs = lpforms.models.FormSimple
mft = lpforms.models.FormText

domain_search = 'yandex'
field_search = 'f2'

SQL_SEARCH_DOMAIN = 'domain_id in (select itd.id from lpforms_domain itd ' + \
                    'where itd.domain like %s)'

search_params = ('%' + domain_search + '%',)
domain_fields = mf.objects.extra(where=[SQL_SEARCH_DOMAIN], params=search_params)

field = mf.objects.filter(fname__icontains=field_search)
field_id = field.values()[0]['id']


for domain_field in domain_fields:
    if domain_field.id == field_id:
        print('\nyes: ' + str(domain_field))
    else:
        print('\nno: ' + str(domain_field))

fields = domain_fields.filter(id=field_id)
print(fields)