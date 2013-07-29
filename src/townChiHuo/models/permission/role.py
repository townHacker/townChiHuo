#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from mongoengine import *

from townChiHuo.models import model
from townChiHuo.models.error import GeneralError
from townChiHuo.util import mongodb_hack as db_hack
import townChiHuo.db_schema as db_schema


class Role(Document):
    '''
    角色
    role_id # 角色id
    name # 角色名称
    description # 角色描述
    parent_roles # 父级角色

    disabled # 是否禁用
    '''
    role_id = UUIDField(binary=False, required=True,
                        unique=True, default=uuid.uuid4())
    name = StringField(max_length=200, required=True)
    description = StringField(max_length=1000)
    parent_roles = ListField(ReferenceField('self'))
    disabled = BooleanField()
    

    meta = { 'collection': db_schema.ROLE }

def get_roles_count():
    return Role.objects(__raw__={'disabled': {'$ne': True}}).count()

def get_roles(limit=None, skip=0):

    if limit or limit == 0:
        cursor = Role.objects(__raw__={'disabled': { '$ne': True }}).limit(limit).skip(skip)
    else:
        cursor = Role.objects(__raw__={'disabled': { '$ne': True }}).skip(skip)
    for r in cursor:
        yield r
            

def _get_role(role_id):
    '''
    获取指定role_id的Role对象
    '''
    return Role.objects(role_id=role_id).first()
        

def _get_roles_without_disabled(*role_parent_ids):
    '''
    获取指定role_id序列中的所有未禁用的role文档
    '''
    return Role.objects(__raw__={
            'role_id': {'$in': role_parent_ids},
            'disabled': {'$ne': True},
            })


def _get_roles_with_disabled(*role_parent_ids):
    '''
    获取指定role_id序列中的所有的role文档(包括已禁用的)
    '''
    return Role.objects(__raw__={
            'role_id': {'$in': role_parent_ids},
            })


def role_add(role_name, role_desc, *role_parent_ids):
    '''
    添加角色
    '''
    if Role.object(__raw__={'name': role_name}).first() \
       is not None:
        # 角色名存在
        raise GeneralError(u'角色名称已存在')
    else:
        # 角色名称不存在, 添加该角色
        role_m = Role(role_name, description=role_desc)
        role_m.parent_roles = [] # 父级角色
        for p_role in \
            _get_roles_without_disabled(*role_parent_ids):
            role_m.parent_roles.append(p_role)
            
        # 若无父级角色, 删除该属性
        if len(role_m.parent_roles) <= 0: del role_m.parent_roles
        
        role_m.save()
        return role_m



def role_remove(*role_ids):
    '''
    删除角色, 设置 disabled = True
    '''
    if role_ids is None:
        raise GeneralError(u"参数错误")

    result = Role.objects().update(
        {'role_id': {'$in': role_ids}},
        {'$set': {
            'disabled': True
        }}
    )
    # result:
    # {u'updatedExisting': True, u'connectionId': 39, u'ok': 1.0, u'err': None, u'n': 1}
    # {u'updatedExisting': False, u'connectionId': 39, u'ok': 1.0, u'err': None, u'n': 0}
    return result['n'] # 返回更新数目

