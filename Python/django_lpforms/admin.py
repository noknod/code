# -*- coding: utf-8 -*- 

from django.contrib import admin



# Register your models here.

from .models import Domain, DomainForm, FormSimple, FormText
from .consts import ADMIN_DOMAINFORM_EXTRA, SQL_SEARCH_DOMAIN



class DomainFormInline(admin.TabularInline):
    model = DomainForm
    extra = ADMIN_DOMAINFORM_EXTRA



class DomainAdmin(admin.ModelAdmin):
    """ Представление таблицы доменных имён при администрировании  """

    list_display = ('domain', 'read_template',)

    list_filter = ('domain',)

    search_fields = ('domain',)

    inlines = [DomainFormInline]



class DomainFormAdmin(admin.ModelAdmin):
    """ Представление таблицы форм при администрировании  """

    fieldsets = [
        (None,             {'fields': ['domain', 'fname']}),
        ('Характеристики', {'fields': ['ftype', 'length', 'required'], 
                            #'classes': ['collapse']
                            }),
    ]

    list_display = ('read_domain', 'fname', 'read_ftype', 'required',)

    list_filter = ('domain',)

    search_fields = ('domain_id__domain', '^fname',)



class FormSimpleAdmin(admin.ModelAdmin):
    """ Представление таблицы простых значений форм при администрировании  """

    list_display = ('read_domain', 'message_id', 'read_field', 'fvalue',)

    list_filter = ('field_id',)

    search_fields = ('^field_id__fname', 'message_id',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(FormSimpleAdmin, 
                       self).get_search_results(request, queryset, search_term)
        terms = search_term.split()
        for domain_term in search_term.split():
            params = ('%' + domain_term + '%',)
            domain_fields = DomainForm.objects.extra(where=[SQL_SEARCH_DOMAIN],
                                                     params=params)
            if len(domain_fields) > 0:
                terms.remove(domain_term)
                for term in ' '.join(terms).split():
                    field = DomainForm.objects.filter(fname__icontains=term)
                    if len(field) > 0:
                        terms.remove(term)
                        domain_fields = domain_fields.filter(id=field[0].id)
                        break
                if len(terms) == 0:
                    for domain_field in domain_fields:
                        queryset |= self.model.objects.filter(
                                                      field_id=domain_field.id)
                elif len(terms) == 1:
                    try:
                        message_id = int(terms[0])
                    except ValueError:
                        pass
                    else:
                        for domain_field in domain_fields:
                            queryset |= self.model.objects.filter(
                                                      field_id=domain_field.id,
                                                      message_id=message_id)
                break
        return queryset, use_distinct



class FormTextAdmin(admin.ModelAdmin):
    """ Представление таблицы полного текста форм при администрировании  """

    list_display = ('read_domain', 'message_id', 'read_field', 'fvalue')

    list_filter = ['field_id']

    search_fields = ['^field_id__fname']



admin.site.register(Domain, DomainAdmin)
admin.site.register(DomainForm, DomainFormAdmin)
admin.site.register(FormSimple, FormSimpleAdmin)
admin.site.register(FormText, FormTextAdmin)