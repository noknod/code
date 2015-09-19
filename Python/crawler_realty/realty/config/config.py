# -*- coding: utf-8 -*- 


import os
import json



class Config(object):
    """ Класс для получения параметров (шаблон Singleton) """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """ Переопределение метода __new__ для реализации шаблона Singleton """
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def __init__(self, error_handler):
        """ Создание объекта класса """
        self.error_handler = error_handler
        self.config = self._read_config_json()

    def read(self, option_path):
        """ 
        Возвращает значение настройки по пути option_path, или None, если 
        таковой не задано.
        """
        config = self.config
        if config is not None:
            option_list = option_path.split(u'.')
            for option in option_list:
                config = config.get(option, None)
                if config is None:
                    break
        return config

    def _read_config_json(self):
        """ Чтение конфигурационного файла формата json """
        config_file = os.path.join(os.path.dirname(__file__), u'config.json')
        try:
            with open(config_file, 'r') as json_file:
                return json.load(json_file, 'utf-8')
        except Exception as e:
            self.error_handler.add_error_and_process(
                {u"error": e, u"source": u"config.py/Config._read_config_json"})
            return None