# -*- coding: utf-8 -*- 


from realty.config.config import Config
from realty.utils import errorhandler
from realty.models.db import get_database
from realty.models.projectDAO import ProjectDAO
from realty.models.infoDAO import InfoDAO

error_handler = errorhandler.get_error_handler()

config = Config(error_handler)

database = get_database(config)

projects = ProjectDAO(database, error_handler)
project_code = u'irr.ru'
code = u'general'
project = projects.get(project_code, code)
print '*project\n', project


params = project[u"params"][0]
info_project = {u"_id": project[u"_id"], u"params": params}
infos = InfoDAO(database, error_handler, info_project)
print '*info\n', list(infos.get_all())

info = {u"asd": "info from asd"}
result = infos.push_info(info)
print u'\n*push return\n', result.modified_count

info = {u"qwe": "info from qwe"}
result = infos.push_info(info)
print u'\n*push return\n', result.modified_count

result = infos.end()
print u'\n*end return\n', result.modified_count

print u'\n*filter return\n', list(infos.get_all())