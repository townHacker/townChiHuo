#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

import settings
import pymongo


__host = settings.settings['mongodb.host']
__port = settings.settings['mongodb.port']
__db_name = settings.settings['mongodb.db']

def connect(host=None, port=None, db=None, collection=None):
    '''
    指定mongodb的host, port, db(数据库名), collection(集合名称)
    若collection为None, 则返回pymongo database对象
    若collection不为None, 则返回指定的 collection 集合对象
    '''
    if host is None:
        host = __host
    if port is None:
        port = __port
    if db is None:
        db = __db_name
    mongo_conn = MongoClient(host, port) # 创建连接
    database = mongo_conn[db]
    if collection:
        return database[collection]
    else:
        return database

