# -*- coding: utf-8 -*- 


from realty.utils.errorhandler import get_error_handler

error_handler = get_error_handler()

try:
	1 / 0
except Exception as e:
    error_handler.add_error_and_process({"error": e, "source": "errorhandler_test.py: 1"})

print error_handler.pop()


def process_last_error(error):
    print error
    return False

error_handler = get_error_handler(process_last_error)

try:
    1 / 0
except Exception as e:
    error_handler.add_error_and_process({"error": e, "source": "errorhandler_test.py: 2"})


print error_handler.pop()