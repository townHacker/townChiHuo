#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Model(dict):
    '''
    模型基类，所有的模型类都应该继承该类
    '''
    def __init__(self, doc=None):
        # 单下划线开关的成员变量为保护变量，只有类及子类可以访问
        if doc is None:
            doc = {}
        self.__dict__["_doc"] = doc

    def __iter__(self):
        return iter(self.__dict__["_doc"])

    def __getitem__(self, name):
        return self.__dict__["_doc"].__getitem__(name)
        
    def __setitem__(self, name, value):
        self.__dict__["_doc"].__setitem__(name, value)

    def __delitem__(self, name):
        self.__dict__["_doc"].__delitem__(name)

        
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

    def __repr__(self):
        return repr(self.__dict__["_doc"])

    def __call__(self):
        return self.__dict__["_doc"]


    def __nonzero__(self):
        return True


    def get_doc(self):
        return self.__dict__["_doc"]


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



if __name__ == '__main__':
    m = Model()
    print m.__dict__
    m.a = 'abc'
    print m._doc['a']
    print m._doc
    d = {'name': 'zhouyunchang'}
#    global model
    user = Model(d)
    print 'getDoc():', user.get_doc()
    print user.name
    import memcache
    mc = memcache.Client(['127.0.0.1:11211'])
    mc.set('model', user)
    u = mc.get('model')
    print u
    print u.name
    if Model():
        print 'True'
    else:
        print 'False'
            
