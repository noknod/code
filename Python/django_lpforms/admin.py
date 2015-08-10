# -*- coding: utf-8 -*- 

from django.contrib import admin



# Register your models here.

from .models import Domain, DomainForm
from .consts import ADMIN_DOMAINFORM_EXTRA



class DomainFormInline(admin.TabularInline):
    model = DomainForm
    extra = ADMIN_DOMAINFORM_EXTRA



class DomainAdmin(admin.ModelAdmin):
    """ Представление таблицы доменных имён при администрировании  """

    pass

    inlines = [DomainFormInline]



class DomainFormAdmin(admin.ModelAdmin):
    """ Представление таблицы форм при администрировании  """

    fieldsets = [
        (None,             {'fields': ['domain', 'fname']}),
        ('Характеристики', {'fields': ['ftype', 'length', 'required'], 
                            #'classes': ['collapse']
                            }),
    ]

    list_display = ('read_domain', 'fname', 'read_ftype', 'required')

    list_filter = ['domain']



admin.site.register(Domain, DomainAdmin)
admin.site.register(DomainForm, DomainFormAdmin)