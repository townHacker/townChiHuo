#!/usr/bin/env python
# -*- coding: utf-8 -*-
__metaclass__ = type

import uuid
import datetime
import time

from mongoengine import *

from townChiHuo.models.permission import Role
from townChiHuo.models.error import GeneralError
from townChiHuo.util import encrypt
from townChiHuo.util import mongodb_hack as db_hack
from townChiHuo import settings
import townChiHuo.db_schema as db_schema

__md5key = settings.settings['password.md5key']

class LoginInfo(EmbeddedDocument):
    '''
    登录信息
    '''
    login_timestamp = IntField()
    last_login_dt = DateTimeField()

class User(Document):
    '''
    用户
    user_id = None
    name # 用户名
    email # 邮箱
    password # 密码
    last_name # 姓
    first_name # 名
    gender # 性别
    role # 用户角色
    login_info # 用户登录信息

    disabled #禁用/启用
    disabled_desc # 禁用描述
    disabled_date # 禁用日期
    '''
    name = StringField(max_length=200, required=True)
    email = StringField(max_length=100, required=True)
    password = StringField(required=True)
    last_name = StringField()
    first_name = StringField()
    gender = StringField()
    role = ReferenceField(Role)
    login_info = EmbeddedDocumentField(LoginInfo)
    disabled = BooleanField()
    disabled_desc = StringField()
    disabled_date = DateTimeField()

    meta = {
        'collection': db_schema.USER,
        'allow_inheritance': True
    }
    
        
def user_add(name, password):
    '''
    添加用户
    '''
    name = unicode(name)
    user = User.objects(__raw__={'name': name}).first()
    if user is not None:
        # 用户名已存在
        raise GeneralError(u'用户名已存在')
    else:
        # 添加用户
        user = User()
        user.name = name
        user.password = encrypt.md5(password, __md5key)
        user.save()
        
        return user
        
       
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
    
    user = User.objects(__raw__={'name': unicode(u_name), \
             'password': encrypt.md5(password, __md5key)}).first()
    if user is None:
        # 用户名密码不正确或用户不存在
        raise GeneralError(u'用户名密码不正确或用户不存在')
    else:
        # 验证登录时间戳
        is_succeed = False
        if user.login_info and \
                user.login_info.login_timestamp:
            is_succeed = user.login_info.login_timestamp == timestamp
        else:
            is_succeed = True
            
        if is_succeed:
            update_login_info(user, record)
            user.save()
        else:
            raise GeneralError(u'登录失败')
            
        return user

        
def register(email, password):
    '''
    用户注册
    email: 邮箱
    password: 密码
    '''
    if None is not \
       User.objects(__raw__={'email': unicode(email)}).first():
        raise GeneralError(u'该邮箱已经注册过，请使用其它邮箱注册.')
    else:
        user = User()
        user.email, user.name = unicode(email), unicode(email)
        user.password = encrypt.md5(password, __md5key)
        
        user.save()
        return user
        
    
                
def update_login_info(user, record=False):
    '''
    更新最后登录时间， 登录时间戳
    '''
    if not user.login_info:
        user.login_info = LoginInfo()
    user.login_info.last_login_dt = datetime.datetime.now()
    if record:
        user.login_info.login_timestamp = \
            time.mktime(user.login_info.last_login_dt.timetuple())
			
			
			
def set_user_available(disabled, *user_ids):
    '''
    禁用用户, 设置 disabled = True
    启用用户, 设置 disabled = False
    '''
    if user_ids is None:
        raise GeneralError(u'参数错误.')
    result = User.objects().update(__raw__=
        {
            {'id': {'$in': user_ids}},
            {'$set': {
                'disabled': disabled
            }}
        }
    )
    return result['n']
    

def user_edit(user_id,name,email,password,last_name,first_name,sex):
    '''
    编辑用户
    '''
    user=User.objects(__raw__={'user_id':user_id}).first()
    if user is None:
        raise GeneralError(u'用户不存在')
	
    
if __name__ == '__main__':
    register('admin', '123456')
