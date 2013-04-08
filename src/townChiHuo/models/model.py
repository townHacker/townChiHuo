#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Model(object):
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

    def __getstate__(self):
        '''
        for pickle, fix python memcached bug
        '''
        return self.__dict__["_doc"]

    def __setstate__(self, state):
        '''
        for pickle, fix python memcached bug
        '''
        self.__dict__["_doc"] = state




def model(doc, m_type=Model):
    '''
    将一个document(mongoDB中的Document)初始为对象
    '''
    m = Model(doc=doc)
    m.__class__ = m_type
    return m


def iter(docs):
    '''
    遍历一个mongoDb document集合,
    返回一个生成器
    '''
    for doc in list(docs):
        yield Model(doc=doc)


def query(collection, **kwargs):
    '''
    查询
    '''
    docs = collection.find(kwargs)
    for doc in docs:
        yield model(doc)


def insert(collection, m):
    '''
    插入
    '''
    return collection.insert(m.__dict__['_doc'])

def remove(collection, m):
    '''
    删除
    '''
    doc = collection.remove(m.__dict__['_doc'])
    if doc:
        doc = model(doc)
    return doc


def save(collection, m):
    '''
    若存在_id则更新, 否则添加
    '''
    return collection.save(m.__dict__['_doc'])
    



if __name__ == '__main__':
    m = Model()
    print m.__dict__
    m.a = 'abc'
    print m._doc['a']
    print m._doc
    d = {'name': 'zhouyunchang'}
#    global model
    user = model(d)
    print user.name
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'])
    mc.set('model', user)
    u = mc.get('model')
    print u
    print u.name
