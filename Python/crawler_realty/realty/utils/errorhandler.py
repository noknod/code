# -*- coding: utf-8 -*- 


import traceback



class ErrorHandler(object):
    """ Класс для получения параметров (шаблон Singleton) """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Переопределение метода __new__ для реализации шаблона Singleton """
        if not cls._instance:
            cls._instance = super(ErrorHandler, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self, process_last_error=None):
        """ Создание объекта класса """
        self.error_list = []
        if process_last_error is not None:
            self.process_last_error = process_last_error
        else:
            self.process_last_error = self._process_last_error

    def add_error_and_process(self, error_json):
        """ Добавляет ошибку в стэк и вызывает обработчик для неё """
        self.error_list.append(error_json)
        while self.process_last_error(self.pop()):
            pass

    def pop(self):
        """ Возвращает и удаляет из стэка последнюю ошибку """
        return self.error_list.pop() if len(self.error_list) > 0 else None

    def _process_last_error(self, error):
        """ Обработка последней ошибки в стэке """
        if error is None:
            return False
        try:
            # source
            print u'\n*error:', error['source']

            # the exception instance
            error = error['error']
            error = traceback.format_exception(type(error), error, None)[0].strip()
            print error + u'*\n'

            ## arguments stored in .args
            #print error['error'].args, u'\n*\n'
            #print u'*\n'
        except:
            traceback.print_exc()
        finally:
            return False



def get_error_handler(process_last_error=None):
    """ Создаёт и возвращает обработчик ошибок """
    return ErrorHandler(process_last_error)