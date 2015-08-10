from django.shortcuts import render_to_response

from django.core.context_processors import csrf
from django.http.response import HttpResponse,  HttpResponseForbidden

from django.db import models, transaction
from django.contrib import admin


from django.core.management import color

from django.db import connection, transaction
from django.core.management.color import no_style

#from django.contrib.contenttypes.models import ContentType

from django.utils.module_loading import import_module
from django.db.models import get_models
from django.conf import settings
from django.conf.urls import include, url


import re


from . import utils



# Create your views here.


def form(request):
    template = 'form.html'
    data = {}
    data.update(csrf(request))
    return _response_(template, data)


def create(request):
    #template = 'ct.html'
    #data = {}
    #data.update(csrf(request))
    if request.method == 'POST':
        table = request.POST.get('table')
        if utils.RE_MACTH_TABLE_NAME.match(table) is None:
            return  HttpResponseForbidden(
                'Название таблицы "' + table + '" не допустимо!', 
                content_type='text/plain')
        keys = list(request.POST.keys())
        keys.remove('table')
        fields = []
        str_fields = []
        for key in keys:
            fname, fstype, flength = request.POST[key].split(',')
            if utils.RE_MACTH_FIELD_NAME.match(fname) is None:
                return  HttpResponseForbidden(
                    'Наименование поля "' + fname + '" не допустимо!', 
                    content_type='text/plain')
            try:
                ftype = utils.FIELD_TYPES[fstype]
            except:
                return  HttpResponseForbidden(
                    'Тип поля "%s" не распознан ("%s")!' % (fname, fstype), 
                    content_type='text/plain')
            try:
                flength = int(flength.replace('-', 'a'))
            except:
                return  HttpResponseForbidden(
                    'Указанная длина поля "%s" не является целым положительным числом!' % (fname), 
                    content_type='text/plain') 
            fields.append(fname + ',' + fstype + ',' + str(flength))
        str_fields = ';'.join(fields)
        errors = utils.dynamic_create_model(table, str_fields)
        #utils.clear_str_created_models()
        #utils.load_at_startup()
        #print('\n\n****\ncode:', code, '; result_register', result_register, '\n')
        if len(errors) == 0:
            return  HttpResponse(table + ' создана', content_type='text/plain')
        else:
            msg = 'При создании таблицы "%s" возникли ошибки:' % (table) + \
                  '\n\n'.join(erorrs)
            return  HttpResponseForbidden(msg, content_type='text/plain')



def _response_(template, data=None):
    return render_to_response(template, data)
