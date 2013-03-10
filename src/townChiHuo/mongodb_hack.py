#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

import settings
from pymongo import MongoClient

class MongoHack:
    host = settings.settings['mongodb.host']
    port = settings.settings['mongodb.port']
    
    mongo_conn = None
    database = settings.settings['mongodb.db']
    collection = None
    def __init__(self, db=None, collection=None):
        '''
        初始化mongoDB, 若有指定的db, collection参数则创建database, collection
        '''
        mongo_conn = MongoClient(host, port)
        if db is not None:
            self.database(db)
            if collection is not None:
                self.collection(collection)

        
    def database(self, db):
        '''
        初始化database
        '''
        self.database = mongo_conn[db]
        return self.database

    def collection(self, collection):
        '''
        初始化collection
        '''
        self.collection = self.database[collection]
        return self.collection

    def insert(self, model, db=None, collection=None):
        '''
        向数据中插入一个对象,可以指定插入的数据库与集合.
        返回：插入对象的 ObjectId
        '''
        if db is not None:
            self.database(db)
        if collection is not None:
            self.collection(collection)
            
        return self.collection.insert(model)

    def save(self, model, db=None, collection=None):
        '''
        保存一个对象，若对象已有ObjectId则update,若没有则insert
        '''
        if db is not None:
            self.database(db)
        if collection is not None:
            self.collection(collection)

        return self.collection.save(model)
