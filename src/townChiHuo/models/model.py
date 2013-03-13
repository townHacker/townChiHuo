#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

def model(doc):
    '''
    将一个document(mongoDB中的Document)初始为对象
    '''
    return Model(doc=doc)


def query(collection, **kwargs):
    '''
    查询
    '''
    docs = collection.find(kwargs)
    for doc in docs:
        yield model(doc)


def insert(collection, model):
    '''
    插入
    '''
    return collection.insert(model.__dict__['_doc'])

def remove(collection, model):
    '''
    删除
    '''
    doc = collection.remove(model.__dict__['_doc'])
    m_fun = global model
    if doc:
        doc = m_fun(doc)
    return doc


def save(collection, model):
    '''
    若存在_id则更新, 否则添加
    '''
    return collection.save(model.__dict__['_doc'])
    

class Model:
    '''
    模型基类，所有的模型类都应该继承该类
    '''
    def __init__(self, doc=None):
        # 单下划线开关的成员变量为保护变量，只有类及子类可以访问
        if doc is None:
            doc = {}
        self.__dict__["_doc"] = doc

    
    def __setattr__(self, name, value):
        '''-
        设置属性
        '''
        self.__dict__["_doc"][name] = value

    
    def __getattr__(self, name):
        '''
        获取属性
        '''
        # 如果字典中不存在键name, 默认返回None
        return self.__dict__["_doc"].get(name)
        

    def __delattr__(self, name):
        '''
        删除属性
        '''
        if self.__dict__["_doc"].get(name) is None:
            return
        else:
            del self.__dict__["_doc"][name]



if __name__ == '__main__':
    m = Model()
    print m.__dict__
    m.a = 'abc'
    print m._doc['a']
    print m._doc
    d = {'name': 'zhouyunchang'}
    global model
    user = model(d)
    print user.name
