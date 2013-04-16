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
import townChiHuo.db_schema as db_schema

__md5key = settings.settings['password.md5key']

class User(model.Model):
    '''
    用户
    user_id = None
    name # 用户名
    email # 邮箱
    password # 密码
    last_name # 姓
    first_name # 名
    sex # 性别
	
	disabled #禁用/启用
    role # 用户角色
    login_info # 用户登录信息
    '''
    def __init__(self, doc=None):
        super(User, self).__init__(doc=doc)

        
def user_add(name, password):
    '''
    添加用户
    '''
    users = db_hack.connect(collection=db_schema.USER)
    name = unicode(name)
    user = users.find_one({'name': name})
    if user is not None:
        # 用户名已存在
        raise GeneralError(u'用户名已存在')
    else:
        # 添加用户
        user = User()
        user.user_id = unicode(uuid.uuid4())
        user.name = name
        user.password = encrypt.md5(password, __md5key)
    try:
        objectId = users.insert(user.get_doc())
        return User(doc=users.find({'_id': objectId}))
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
    if not u_name or not password:
        raise GeneralError(u'请填写正确的用户名密码')
    
    users = db_hack.connect(collection=db_schema.USER)
    user = users.find_one({'name': unicode(u_name), \
             'password': encrypt.md5(password, __md5key)})
    if user is None:
        # 用户名密码不正确或用户不存在
        raise GeneralError(u'用户名密码不正确或用户不存在')
    else:
        # 验证登录时间戳
        user = User(doc=user) # User object
        is_succeed = False
        if user.login_info and \
                user.login_info.get('login_timestamp'):
            is_succeed = user.login_info['login_timestamp'] == timestamp
        else:
            is_succeed = True
            
        if is_succeed:
            update_login_info(user, record)
            users.save(user.get_doc())
        else:
            raise GeneralError(u'登录失败')
            
        return user

        
def register(email, password):
    '''
    用户注册
    email: 邮箱
    password: 密码
    '''
    users = db_hack.connect(collection=db_schema.USER)
    if None is not \
            users.find_one({'email': unicode(email)}):
        raise GeneralError(u'该邮箱已经注册过，请使用其它邮箱注册.')
    else:
        user = User()
        user.user_id = unicode(uuid.uuid4())
        user.email, user.name = unicode(email), unicode(email)
        user.password = encrypt.md5(password, __md5key)
        try:
            objectId = users.insert(user.get_doc())
            return User(doc=users.find({'_id': objectId}))
        finally:
            del users
        
    
                
def update_login_info(user, record=False):
    '''
    更新最后登录时间， 登录时间戳
    '''
    user.login_info = {'last_login_dt': datetime.datetime.now()}
    if record:
        user.login_info['login_timestamp'] = \
            time.mktime(user.login_info['last_login_dt'].timetuple())
			
			
			
def user_remove(disabled,*user_ids):
    '''
    删除用户, 设置 disabled = True
    '''
    if user_ids is None:
        raise GeneralError(u'参数错误.')
    user_c = db_hack.connect(collection=db_schema.USER)
    try:
        result = user_c.update(
            {'user_id': {'$in': user_ids}},
            {'$set': {
                    'disabled': disabled
                    }}
            )
        return result['n']
    finally:
        del user_c

def user_edit(user_id,name,email,password,last_name,first_name,sex):
    '''
    编辑用户
    '''
    user_c = db_hack.connect(collection=db_schema.USER)
    user=user_c.find_one({'user_id':user_id})
    if user is None:
        raise GeneralError(u'用户不存在')
	
    
if __name__ == '__main__':
    register('admin', '123456')
