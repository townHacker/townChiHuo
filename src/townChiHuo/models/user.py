#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

import uuid
import datetime
import time
from hashlib import md5

from townChiHuo.mongodb_hack import mongodb_hack as db_hack
from townChiHuo.models import model

class User(model.Model):
    '''
    用户
    user_id = None
    user_name # 用户名
    email # 邮箱
    password # 密码
    last_name # 姓
    first_name # 名
    sex # 性别

    role # 用户角色
    login_info # 用户登录信息
    '''

def login(u_name, password, timestamp=None, record=False):
    '''
    用户登录
    u_name: 用户名
    password: 密码
    timestamp: 登录时间戳
    record: 是否需要记录登录时间戳
    '''
    users = db_hack.connect(collection='users')
    user = users.find_one( \
        {'name': u_name, \
             'password': password})
    if user is None:
        # 用户名密码不正确或用户不存在
        return False
    else:
        # 验证登录时间戳
        is_succeed = False
        if user.login_info.login_timestamp is not None:
            is_succeed = user.login_info.login_timestamp == timestamp
        else:
            is_succeed = True
            
            if is_succeed:
                update_login_info(user, record)
                users.save(user)
            return is_succeed

        
def register(email, password):
    '''
    用户注册
    email: 邮箱
    password: 密码
    '''
    
    user = User()
    user.email, user.name = email, email
    user.password = md5(password)
    users = db_hack.connect(collection='users')

    if None is not \
            users.find_one({'email': email}):
        raise Exception('该邮箱已经注册过，请使用其它邮箱注册.')
    else:
        objectId = users.insert(user)
        return users.find({'_id': objectId})
    
            
        
def md5(password):
    '''
    生成md5加密后的密码，返回加密后的密码
    '''
    md5key = settings.settings['password.md5key']
    m = md5()
    m.update(md5key + password)
    return m.digest()
    
                
def update_login_info(user, record=False):
    '''
    更新最后登录时间， 登录时间戳
    '''
    user.login_info.last_login_dt = datetime.datetime.now()
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
