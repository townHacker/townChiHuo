#!/usr/bin/env python
# -*- coding: utf-8 -*-
__metaclass__ = type

import uuid
import datetime
import time

from townChiHuo.models import model
from townChiHuo.models.error import GeneralError
from townChiHuo.util import encrypt
from townChiHuo.util import mongodb_hack as db_hack
from townChiHuo import settings

__md5key = settings.settings['password.md5key']

class User(model.Model):
    '''
    用户
    id = None
    name # 用户名
    email # 邮箱
    password # 密码
    last_name # 姓
    first_name # 名
    sex # 性别

    role # 用户角色
    login_info # 用户登录信息
    '''

def user_add(name, password):
    '''
    添加用户
    '''
    users = db_hack.connect(collection='users')
    name = unicode(name)
    user = users.find_one({'name': name})
    if user is not None:
        # 用户名已存在
        raise GeneralError(u'用户名已存在')
    else:
        # 添加用户
        user = User()
        user.name = name
        user.password = encrypt.md5(password, __md5key)
    try:
        objectId = model.insert(users, user)
        return users.find({'_id': objectId})
    finally:
        del users
        
       
def login(u_name, password, timestamp=None, record=False):
    '''
    用户登录
    u_name: 用户名
    password: 密码
    timestamp: 登录时间戳
    record: 是否需要记录登录时间戳
    '''
    users = db_hack.connect(collection='users')
    user = users.find_one({'name': unicode(u_name), \
             'password': encrypt.md5(password, __md5key)})
    if user is None:
        # 用户名密码不正确或用户不存在
        raise GeneralError(u'用户名密码不正确或用户不存在')
        return False
    else:
        # 验证登录时间戳
        user = model.model(user) # User object
        is_succeed = False
        if user.login_info and \
                user.login_info.get('login_timestamp'):
            is_succeed = user.login_info['login_timestamp'] == timestamp
        else:
            is_succeed = True
            
        if is_succeed:
            update_login_info(user, record)
            model.save(users, user)
            
        return is_succeed

        
def register(email, password):
    '''
    用户注册
    email: 邮箱
    password: 密码
    '''
    users = db_hack.connect(collection='users')
    if None is not \
            users.find_one({'email': unicode(email)}):
        raise GeneralError(u'该邮箱已经注册过，请使用其它邮箱注册.')
    else:
        user = User()
        user.id = unicode(uuid.uuid4())
        user.email, user.name = unicode(email), unicode(email)
        user.password = encrypt.md5(unicode(password), __md5key)
        try:
            objectId = model.insert(users, user)
            return users.find({'_id': objectId})
        finally:
            del users
        
    
                
def update_login_info(user, record=False):
    '''
    更新最后登录时间， 登录时间戳
    '''
    user.login_info = {'last_login_dt': datetime.datetime.now()}
    if record:
        user.login_info.login_timestamp = \
            time.mktime(user.login_info.last_login_dt.timetuple())
    

class LoginInfo:
    '''
    登录信息
    last_login_dt  # 最后一次登录时间
    login_timestamp  # 登录时间戳
    '''
    
    
if __name__ == '__main__':
    register('admin', '123456')
