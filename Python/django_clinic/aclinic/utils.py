# -*- coding: utf-8 -*- 


import re
import traceback

from django.db import transaction


from aclinic.consts import RE_ONLY_ALPHA_AND_SPACE, RE_ONLY_ONE_SPACE, \
        DB_TABLE_PREFIX, DB_USING, DB_SQLITE, DB_POSTGRESQL



def fio_clean(fio):
    """ Очистка и преобразование ФИО к виду 'Слово Слово...' """
    fio = RE_ONLY_ONE_SPACE.sub(' ', 
            RE_ONLY_ALPHA_AND_SPACE.sub('', fio.lower()))
    return fio.strip().title()



# Создание функции для получения следующего значения последовательности, 
# которую представляет модель model
if DB_USING == DB_SQLITE:

    from queue import Queue
    from threading import Thread


    def do_work_sequence(model):
        nextval = model.objects.get_or_create(id=1)[0]
        nextval.nextval += 1
        nextval.save()
        return nextval.nextval


    def worker_sequence():
        while True:
            try:
                model, retobject = queue_sequence.get()
                nextval = do_work_sequence(model)
                retobject.nextval = nextval
            except Exception as e:
                print('\n***ERROR: \n')
                traceback.print_exc()
            finally:
                queue_sequence.task_done()


    queue_sequence = Queue()
    thread_sequence = Thread(target=worker_sequence)
    thread_sequence.daemon = True
    thread_sequence.start()


    class RetObject(object):
        nextval = 0


    def get_nextval_from_sequence_sl(model):
        """
        Возвращает следующее значение последовательности (sequence) из SQLite, 
        которая задана моделью model
        """
        nextval = RetObject()
        queue_sequence.put([model, nextval])
        queue_sequence.join()
        return nextval.nextval


    get_nextval_from_sequence = get_nextval_from_sequence_sl


elif DB_USING == DB_POSTGRESQL:
    
    def get_nextval_from_sequence_ps(model):
        """
        Возвращает следующее значение последовательности (sequence) из 
        PostgreSQL, которая задана моделью model
        """
        seq =  model._meta.db_table
        pref = DB_TABLE_PREFIX
        sql = "select sequence_name, nextval('{seq}') from {pref}{seq}".format(
               seq=seq, pref=pref)
        return model.objects.raw(sql)[0].nextval


    get_nextval_from_sequence = get_nextval_from_sequence_ps



def get_user_ip_address(request):
    """ Возвращает словарь с ip-адресом пользователя """
    return {'user_ip_address': request.META['REMOTE_ADDR']}



def get_coupon_from_admission(admission):
    """ Возвращает словарь с данными приёма (талон) """
    coupon = {'reg_num': admission.id,  
              'vdate': admission.schedule_id.read_reception_date(), 
              'hour': admission.schedule_id.read_reception_hour(), 
              'client': admission.read_client(), 
              'doctor': admission.schedule_id.read_doctor()}

    return coupon