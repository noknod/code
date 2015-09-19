# -*- coding: utf-8 -*- 


import pymongo



def get_database(config):
    """ Возвращает соединение к базе данных с настройками из config """
    opts = config.read(u'connection')
    connection = pymongo.MongoClient(opts[u'host'], opts[u'port'])

    if opts[u'user'] != u'':
        connection.the_database.authenticate(opts[u'user'], opts[u'password'], 
                                             mechanism=opts[u'SCRAM-SHA-1'])
    
    database = connection[opts[u'database']]

    return database