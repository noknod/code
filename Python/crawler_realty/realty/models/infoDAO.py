# -*- coding: utf-8 -*- 

from datetime import datetime

from pymongo.collection import ReturnDocument



# The Info Data Access Object handles all interactions 
# with the infos collection.
class InfoDAO:

    def __init__(self, db, error_handler, project_with_params):
        self.db = db
        self.infos = self.db.infos
        self.error_handler = error_handler
        params = project_with_params.get(u"params", None)
        if params is None:
            params = u""
        else: 
            params = params[u"code"]
        vdatetime = datetime.now()
        self.project = {u"project_id": project_with_params[u"_id"], 
                        u"params": params, u"start": vdatetime}
        self.infos.insert_one({u"project_id": project_with_params[u"_id"], 
                u"params": params, u"start": vdatetime, u"info": []})


    def get_all(self):
        """  Возвращает курсор с полученной информацией """

        return self.infos.find(self.project)


    # push a new info into the project`s data
    def push_info(self, info):

        info[u"time"] = datetime.now()

        try:
            result = self.infos.update_one(
                        self.project,
                        {u"$push": {u"info": info}},
                        False
                    )
        except Exception as e:
            self.error_handler.add_error_and_process(
                {u"error": e, 
                 u"source": u"models.infoDAO.py/InfoDAO.push_info"})
            return None

        return result


    def end(self):
        """  Сохраняет время окончания """

        try:
            result = self.infos.update_one(
                        self.project,
                        {u"$set": {u"end": datetime.now()}},
                        False
                    )
        except Exception as e:
            self.error_handler.add_error_and_process(
                {u"error": e, 
                 u"source": u"models.infoDAO.py/InfoDAO.end"})
            return None

        return result