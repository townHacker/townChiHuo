#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

class Model:
    '''
    模型基类，所有的模型类都应该继承该类
    '''
    def __init__(self):
        # 单下划线开关的成员变量为保护变量，只有类及子类可以访问
        self.__dict__["_doc"] = {}

    
    def __setattr__(self, name, value):
        '''-
        设置属性
        '''
        self.__dict__["_doc"][name] = value

    
    def __getattr__(self, name):
        '''
        获取属性
        '''
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
    model = Model()
    print model.__dict__
    model.a = 'abc'
    print model._doc['a']
    print model._doc
