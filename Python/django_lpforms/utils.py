# -*- coding: utf-8 -*- 


import traceback
from django.db import transaction


from lpforms.consts import DB_TABLE_PREFIX, DB_USING, DB_SQLITE, DB_POSTGRESQL



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



def response_error(status, message):
    return (status, message)




class MessagePostManager(object):
    """ Класс для записи в базу данных введённого пользователем сообщения. """

    def __init__(self, mdomain, mform, msequence, msimple, mtext):
        """ 
        mdomain - модель с доменными именами,
        mform - модель с формами,
        msequence - модель с последовательностью,
        msimple - модель с простыми значениями полей,
        mtext - модель с полнотекстовыми значениями полей.
        """
        self.msimple = msimple
        self.mtext = mtext
        self.msequence = msequence
        self.mdomain = mdomain
        self.mform = mform

    def post(self, domain, message):
        """ 
        Сохраняет в базе данных введённое пользователем сообщение.
        domain - наименование или ключ соответствующего доменного имени
        message - сообщение в виде словаря 'поле формы': 'значение'.
        """
        if not isinstance(domain, int):
            domain_id = self._get_domain_id(domain)
            if domain_id is None:
                return response_error(500, 
                                 'Доменное имя "{0}" не задано!'.format(domain))
        else:
            domain_id = domain

        fields = self._read_fields(domain_id, message)
        if fields[0] != 0:
            return response_error(500, 
                   'Поле формы "{1}" для доменного имени "{0}"'.format(domain, 
                    fields[1]) + ' не задано!')

        message_id = get_nextval_from_sequence(self.msequence)
        self._do_post(message_id, fields[1:])


    def _get_domain_id(self, domain):
        """ Возвращает ключ в базе данных для доменного имени domain """
        domain = self.mdomain.objects.filter(domain=domain)
        if len(domain) > 0:
            return domain[0].id
        else:
            return None

    def _get_field_descr(self, domain_id, field):
        """ Возвращает поле формы field доменного имени c ключом domain_id. """
        field = self.mform.objects.filter(domain=domain_id, fname=field)
        if len(field) > 0:
            return field[0]
        else:
            return None

    def _read_fields(self, domain_id, message):
        """ 
        Возвращает список, содержащий для каждого элемента словаря message 
        ключ в базе данных и тип поля формы доменного имени c ключом domain_id 
        и значение введённое пользователем.
        """
        fields = [0]
        for field, fvalue in message.items():
            field_descr = self._get_field_descr(domain_id, field)
            if field_descr is None:
                return (1, field,)
            fields.append((field_descr, fvalue, ))
        return fields
            

    def _do_post(self, message_id, fields):
        """ Сохраняет простое значение в базе данных. """
        with transaction.atomic():
            for field, fvalue in fields:
                if field.ftype in ('TT'):
                    row = self.mtext.objects.create(message_id=message_id, 
                                              field_id=field, fvalue=fvalue)
                else:
                    row = self.msimple.objects.create(message_id=message_id, 
                                              field_id=field, fvalue=fvalue)
                row.save()
#        except Exception as e:
#            transaction.rollback()
#            return (1, e)
#        return (0)
