
from realty.config.config import Config
from realty.utils.errorhandler import get_error_handler
from realty.models.db import get_database


error_handler = get_error_handler()

config = Config(error_handler)

print get_database(config)