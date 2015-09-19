# -*- coding: utf-8 -*- 


from pymongo.collection import ReturnDocument


from realty.utils.utils import code_clean



# The Project Data Access Object handles all interactions 
# with the projects collection.
class ProjectDAO:

    def __init__(self, db, error_handler):
        self.db = db
        self.projects = self.db.projects
        self.error_handler = error_handler

    # find a project corresponding to a project and a particular code
    def get(self, project, code):

        project, code = self._clean_codes(project, code)

        return self.projects.find_one({u'project': project, u'code': code})

    # find a project corresponding to a particular _id
    def get_by_id(self, rid):

        return self.projects.find_one({u'_id': rid})

    # return filtered projects
    def filter(self, filter_json=None):

        if filter_json is None:
            filter_json = {}
        return self.projects.find(filter_json)

    # creates a new project in the projects collection if it is not exists 
    # or replace one
    def upsert_project(self, project, code, scrapy, project_config, info=u''):

        project, code = self._clean_codes(project, code)

        try:
            project = self.projects.find_one_and_update(
                    filter={u"project": project, u"code": code}, 
                    update={u"$set": {u"project": project, u"code": code, 
                                u"scrapy": scrapy, u"config": project_config,
                                u"info": info, u"params": []}}, 
                    upsert=True, 
                    return_document=ReturnDocument.AFTER)
        except Exception as e:
            self.error_handler.add_error_and_process(
                {u"error": e, 
                 u"source": u"models.projectDAO.py/ProjectDAO.upsert_project"})
            return None

        return project
    
    # push a new request parameters in the particular project 
    def push_params(self, project, code, params):

        project = self.get(project, code)

        if project is None:
            return None

        return self.push_params_by_id(project[u'_id'], params)

    # push a new request parameters in the particular project by id
    def push_params_by_id(self, rid, params):

        params[u'code'] = code_clean(params[u'code'])

        try:
            project = self.projects.update_one(
                        {u"_id": rid},
                        {u"$addToSet": {u"params": params}},
                        False
                    )
        except Exception as e:
            self.error_handler.add_error_and_process(
                {u"error": e, u"source": 
                    u"models.projectDAO.py/ProjectDAO.push_params_by_id"})
            return None

        return project

    def _clean_codes(self, project, code):
        """ Возвращает очищенные коды проекта """
        project = code_clean(project).upper()
        code = code_clean(code)

        return project, code