# -*- coding: utf-8 -*- 


import traceback


from .consts import DB_TABLE_PREFIX, DB_USES



def get_nextval_from_sequence_ps(model):
    """
    Возвращает следующее значение последовательности (sequence) из PostgreSQL, 
    которая задана моделью model
    """
    seq =  model._meta.db_table
    prefix = DB_TABLE_PREFIX
    sql = "select sequence_name, nextval('{seq}') from {prefix}{seq}".format(
           seq=seq, prefix=prefix)
    return model.objects.raw(sql)[0].nextval


def get_nextval_from_sequence_sl(model):
    """
    Возвращает следующее значение последовательности (sequence) из SQLite, 
    которая задана моделью model
    """
    nextval = RetObject()
    queue_sequence.put([model, nextval])
    queue_sequence.join()
    return nextval.nextval



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



if DB_USES == 'SQLite':
    from queue import Queue
    from threading import Thread

    queue_sequence = Queue()
    thread_sequence = Thread(target=worker_sequence)
    thread_sequence.daemon = True
    thread_sequence.start()

    class RetObject(object):
        nextval = 0