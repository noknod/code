# -*- coding: utf-8 -*-


import re, subprocess, os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.core.urlresolvers import clear_url_caches
#from django.core.cache import cache
from django.db import connection, models, transaction, IntegrityError, \
                      DatabaseError
from django.db.models.loading import cache as app_cache
from django.utils.module_loading import import_module

from adyncrtbl.models import CreatedTables



""" !!! ВНИМАНИЕ !!! """
""" Переменная отвечает за необходимость проведения миграции в базе 
    после динамического создания модели во время работы сервера
"""
MIGRATE_AFTER_CREATE_MODEL = False



# Постоянные значения для динамического создания модели

## Свойства приложения
APP_LABEL = 'adyncrtbl'
APP_MODULE = 'dyncrtbl.adyncrtbl'

## Кодировка типов полей
INTEGER_FIELD, CHAR_FIELD, TEXT_FIELD = ('0', '1', '2')
FIELD_TYPES = {
    INTEGER_FIELD: {'type' : 'IntegerField', 'field' : models.IntegerField}, 
    CHAR_FIELD: {'type' : 'CharField', 'field' : models.CharField}, 
    TEXT_FIELD: {'type' : 'TextField', 'field' : models.TextField}}

## Регулярное выражение для проверки навзания таблицы
RE_MACTH_TABLE_NAME = re.compile(r'^[a-z]{1,30}$')
## Регулярное выражение для проверки навзания таблицы
RE_MACTH_FIELD_NAME = re.compile(r'^[a-z]+$')

## Свойства создаваемой модели по умолчанию
OPTIONS = {'verbose_name': 'dynamically created: %s'}
ADMIN_OPTS = {}

## Приложение администрирования сайта по умолчанию
ADMIN_SITE = admin.site

## Представления ошибок
ERROR_FIELD_TYPE, ERROR_TABLE_EXIST, ERROR_ADMINURL_CLEAR, \
    ERROR_ADMINURL_RELOAD, ERROR_SAVE_MODEL, ERROR_MIGRATE = range(1, 7)
ERROR_MSGS = {
    ERROR_FIELD_TYPE: 'Тип поля "%s" не распознан (передано "%s")!', 
    ERROR_TABLE_EXIST: 'Таблица "%s" уже есть в базе!', 
    ERROR_ADMINURL_CLEAR: 'Ошибка при очистки ссылок!\n%s', 
    ERROR_ADMINURL_RELOAD: 'Ошибка при обновлении ссылок!\n%s', 
    ERROR_SAVE_MODEL: 
        'Ошибка при сохранении сведений о созданной модели в базе!\n%s', 
    ERROR_MIGRATE: 'Ошибка при выполнении миграции в базе!\n%s'}

## Команды при проведении миграции
MIGRATE_COMMAND_PYTHON = 'python'
MIGRATE_COMMAND_MANAGEPY = os.path.join(settings.BASE_DIR, 'manage.py')
MIGRATE_COMMAND_1 = MIGRATE_COMMAND_PYTHON + ' ' + MIGRATE_COMMAND_MANAGEPY + \
                  ' makemigrations'
MIGRATE_COMMAND_2 = MIGRATE_COMMAND_PYTHON + ' ' + MIGRATE_COMMAND_MANAGEPY + \
                  ' migrate --fake'



# Переменные для хранения сведений о созданных моделях

## Список созданных моделей
created_models = []

## Строка, хранящая созданные модели для передачи клиенту
str_created_models = ''



# Вспомогательные функции

def _get_field_by_type(ftype, flength):
    """ Создание поля для модели по заданному типу. """
    return ftype['field']() if (flength == 0) else \
           ftype['field'](max_length=flength)


def _parse_fields_from_str(str_fields):
    """ Получение словаря полей из строкового представления. """

    fields = {}
    for row in str_fields.split(';'):
        fname, fstype, flength = row.split(',')

        ftype = FIELD_TYPES.get(fstype)
        if ftype is None:
            msg = ERROR_MSGS[ERROR_FIELD_TYPE] % (fname, fstype)
            return (ERROR_FIELD_TYPE, msg)

        fields[fname] = _get_field_by_type(ftype, int(flength))

    return (0, fields)


def _save_created_model_in_base(model_name, str_fields):
    """ Сохранение сведений о созданной динамической модели в базе. """
    if len(CreatedTables.objects.filter(title=model_name)) > 0:
        result_code = ERROR_SAVE_MODEL
        result_msg = ERROR_MSGS[ERROR_TABLE_EXIST] % (model_name)
        result_msg = ERROR_MSGS[result_code] % (result_msg)
        return (result_code, result_msg)
    result_code = 0
    result_msg = ''
    table = CreatedTables(title=model_name, fields=str_fields)
    try:
        table.save()
        transaction.commit()
    except IntegrityError as e:
        transaction.rollback()
        result_code = ERROR_SAVE_MODEL
        result_msg = ERROR_MSGS[result_code] % (str(e))
    return (result_code, result_msg)


def _store__model_in_memory(model_name):
    """ Сохранение сведений о модели в памяти для передачи клиенту. """
    if not model_name in created_models:
        global str_created_models
        created_models.append(model_name)
        created_models.sort()
        str_created_models = ';'.join(created_models)
    return str_created_models


def _migrate_in_db():
    """ Выполнение миграции в базе после динамического создания модели. """
    result_code = 0
    result_msg = ''
    if MIGRATE_AFTER_CREATE_MODEL:
        try:
            subprocess.call(MIGRATE_COMMAND_1)
            subprocess.call(MIGRATE_COMMAND_2)
        except Exception as e:
            result_code = ERROR_MIGRATE
            result_msg = ERROR_MSGS[result_code] % (str(e))
    return (result_code, result_msg)



# Динамическое создание модели

def remove_model_from_cache(model_name, app_label=APP_LABEL):
    """ Удаление заданной модели из кэша моделей. """

    try:
        del app_cache.all_models[app_label][model_name]
    except KeyError:
        pass


def create_model(name, fields=None, app_label='', module='', options=None, 
                 admin_opts=None):
    """ Создание модели в памяти с указанными свойствами 
    (источник https://code.djangoproject.com/wiki/DynamicModels). """

    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    admin_class = None
    if admin_opts is not None:
        class Admin(admin.ModelAdmin):
            pass
        for key, value in admin_opts.items():
            setattr(Admin, key, value)
        admin_class = Admin
    return (model, admin_class)


def create_dbtable_for_model(model):
    """ Создание в базе таблицы (в случае её отсутствия) для модели. """

    table_name = model._meta.db_table

    # Проверка на существование таблицы в базе
    tables = connection.introspection.table_names() 
    if connection.introspection.table_name_converter(table_name) in tables:
        msg = ERROR_MSGS[ERROR_TABLE_EXIST] % (model._meta.model_name)
        return (ERROR_TABLE_EXIST, msg)

    # Создание таблицы в случае отсутствия
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(model)
    return (0, '')



# Регистрация модели в приложении администрирования сайта

def unregister_from_admin(model, site=ADMIN_SITE):
    """ Удаление заданной модели из приложения администрирования. """

    # Сперва удалим текущее описание (модели могут отличаться), 
    # для определения экивалентных классов используем таблицу в базе
    table_name = model._meta.db_table
    keys = []
    for reg_model in site._registry.keys():
        if table_name == reg_model._meta.db_table:
            keys.append(reg_model)
    for key in keys:
            del site._registry[key]

    # Дополнительно применим обычный подход (возможно, излишне)
    try:
        site.unregister(model)
    except NotRegistered:
        pass

    # Перезагрузка конфигурации и очистка кэша ссылок
    return update_admin_urls()


def register_in_admin(model, admin_class=None, site=ADMIN_SITE):
    """ Регистрация динамически созданной модели в приложении 
    администрирования. """

    # Удаление модели из приложения администрирования
    unregister_from_admin(model, site)

    # Регистрация модели    
    site.register(model, admin_class)

    # Перезагрузка конфигурации и очистка кэша ссылок
    return update_admin_urls()


def update_admin_urls():
    """ Перезагрузка конфигурации и очистка кэша ссылок приложения 
    администрирования, иначе все вновь зарегистрированные модели будут 
    недоступны для редактирования. 
    (источник https://pypi.python.org/pypi/django-quickadmin)"""

    # Delete the old admin URLs
    # It's important to use the same string as ROOT_URLCONF
    old_pattern = None
    admin_regex = r'^admin/'
    project_urls = import_module(settings.ROOT_URLCONF)
    result_code = 0
    result_msg = ''
    for url_item in project_urls.urlpatterns:
        try:
            if url_item.app_name == 'admin':
                old_pattern = url_item
                admin_regex = url_item.regex.pattern
                project_urls.urlpatterns.remove(url_item)
                break
        except AttributeError as e:
            # Bypass the non-admin URLconf
            result_code = ERROR_ADMINURL_CLEAR
            result_msg = ERROR_MSGS[result_code] % (str(e))
            #print('\nError when finding and removing old admin URLconf.'
            #print(str(e) + '\n')

    # Reload updated admin URLs
    try:
        admin.autodiscover()
        project_urls.urlpatterns.append(
            url(admin_regex, include(admin.site.urls))
        )
    except Exception as e:
        result_code = ERROR_ADMINURL_RELOAD
        result_msg = ERROR_MSGS[result_code] % (str(e))
        #print('\nError when updating new admin URLconfs.')
        #print(str(e) + '\n')
        if old_pattern:
            project_urls.urlpatterns.append(old_pattern)
    return (result_code, result_msg)



# Основной API для создания и регистрации динамических моделей

def load_at_startup():
    """ Загрузка ранее созданных и сохранённых в базе моделей 
    при запуске сервера. """

    # В случае возможного повторного вызова выходим
    if str_created_models != '':
        return ([], str_created_models)
    print('\n\n*****DO\n\n')

    # Свойства модели по умолчанию
    app_label = APP_LABEL
    module = APP_MODULE
    options = {}
    for key, value in OPTIONS.items():
        options[key] = value
    admin_opts = ADMIN_OPTS

    # Считывание моделей из базы
    errors = []

    try:
        print(CreatedTables.objects.all())
    except Exception as e:
        return (None, 'init migration')
    for row in CreatedTables.objects.all():
        model_name = row.title
        code, fields = _parse_fields_from_str(row.fields)

        # В случае корректности заданных полей создаём модель
        if code == 0:
            # Удаление из кеша (возможно, напрасно)
            remove_model_from_cache(model_name)

            # Создание модели
            options['verbose_name'] = OPTIONS['verbose_name'] % model_name
            model, admin_class = create_model(model_name, fields, app_label, 
                                              module, options, admin_opts)

            # Регистрация модели в приложении для администрирования
            #unregister_from_admin(model)
            code, msg = register_in_admin(model, admin_class)
            #code, msg = update_admin_urls()
            if code != 0:
                errors.append((model_name, code, msg, ))

            # Сохранение сведений о модели в памяти для передачи клиенту
            _store__model_in_memory(model_name)
        else:
            errors.append((model_name, code, fields, ))

    # Вывод возможных ошибок
    if len(errors) > 0:
        print('\nОшибки при загрузки моделей:')
        for error in errors:
            print('\n' + error[0])
            print(error[2])
    return (errors, str_created_models)



def dynamic_create_model(model_name, str_fields):
    """ Динамическое создание модели. """

    # Свойства модели по умолчанию
    app_label = APP_LABEL
    module = APP_MODULE
    options = {}
    for key, value in OPTIONS.items():
        options[key] = value
    admin_opts = ADMIN_OPTS

    print('\n0')
    code, fields = _parse_fields_from_str(str_fields)

    print('\n1')
    errors = []
    # В случае корректности заданных полей создаём модель
    if code == 0:
        # Удаление из кеша
        remove_model_from_cache(model_name)

        print('\n2')

        # Создание модели
        options['verbose_name'] = options['verbose_name'] % model_name
        model, admin_class = create_model(model_name, fields, app_label, 
                                          module, options, admin_opts)

        print('\n3')

        # Создание таблиы в базе
        code, msg = create_dbtable_for_model(model)

        print('\n4')

        if code != 0:
            errors.append(msg)

        # Сохранение сведений о созданной динамической модели в базе
        code, msg = _save_created_model_in_base(model_name, str_fields)

        print('\n5')

        if code != 0:
            errors.append(msg)

        # Регистрация модели в приложении для администрирования
        #unregister_from_admin(model)

        #print('\n6')

        code, msg = register_in_admin(model, admin_class)

        print('\n7')

        #code, msg = update_admin_urls()
        if code != 0:
            errors.append(msg)

        # Сохранение сведений о модели в памяти для передачи клиенту
        _store__model_in_memory(model_name)

        print('\n8')

        # Выполнение миграции
        code, msg = _migrate_in_db()

        print('\n9')

        if code != 0:
            errors.append(msg)
    else:
        errors.append(fields)

    # Вывод возможных ошибок
    if len(errors) > 0:
        print('\nОшибки при создании модели "%s":' % (model_name))
        for error in errors:
            print('\n' + error)
    return errors



"""
print('\n***')
str_fields = 'f1,10,0;f2,1,15'
code, msg = _parse_fields_from_str(str_fields)
print(code, msg)
str_fields = 'f1,0,0;f2,1,15'
code, fields = _parse_fields_from_str(str_fields)
print(code, str_fields)
print('#1 passed')
#"""

"""
print('\n***')
table_name = 'z'
app_label = APP_LABEL
module = APP_MODULE
options = OPTIONS
options['verbose_name'] = options['verbose_name'] % table_name
admin_opts = ADMIN_OPTS
model, admin_class = create_model(table_name, fields, app_label, module, options, admin_opts)
print(model._meta.model_name, model._meta.object_name, model._meta.db_table, 
      model._meta.verbose_name)
print('#2 passed')
#"""

"""
print('\n***')
db_code, msg = create_dbtable_for_model(model)
print(db_code, msg)
print(create_dbtable_for_model(model))
print('#3 passed')
#"""

"""
print('\n***')
unregister_from_admin(model)
register_in_admin(model, admin_class)
update_admin_urls()
print('#4 passed')
#"""

"""
print('\n***')
code, msg = _save_created_model_in_base(model._meta.model_name, str_fields)
print(code, msg)
print(_store__model_in_memory(model._meta.model_name))
print('#5 passed')
#"""

"""
print('\n***')
remove_model_from_cache(model._meta.model_name)
print('#6 passed')
#"""
#_migrate_in_db

def clear_str_created_models():
    global str_created_models
    str_created_models = ''