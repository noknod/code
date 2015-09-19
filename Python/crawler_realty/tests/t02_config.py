# -*- coding: utf-8 -*- 

from realty.utils.errorhandler import get_error_handler
from realty.config.config import Config

error_handler = get_error_handler()

config = Config(error_handler)

print config.read('connection')

print config.read('connection.host')

print config.read("defaults.limit")
