#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from townChiHuo.models import model
from townChiHuo.models.error import GeneralError
from townChiHuo.util import mongodb_hack as db_hack
import townChiHuo.db_schema as db_schema


class Role(model.Model):
    '''
    角色
    role_id # 角色id
    name # 角色名称
    description # 角色描述
    parent_roles # 父级角色
    '''
    def __init__(self, name=None, role_id=None, description=None, doc=None):
        super(Role, self).__init__(doc=doc)
        if not doc: 
            if role_id is None:
                role_id = unicode(uuid.uuid4())
            self.role_id = role_id
            self.name = name
            self.description = description

def get_roles_count():
    return db_hack.connect(collection=db_schema.ROLE) \
        .find({'disabled': {'$ne': True}}).count()

def get_roles(limit=None, skip=0):
    role_c = db_hack.connect(collection=db_schema.ROLE)
    if limit or limit == 0:
        cursor = role_c.find({'disabled': { '$ne': True }}).limit(limit).skip(skip)
    else:
        cursor = role_c.find({'disabled': { '$ne': True }}).skip(skip)
    for r_doc in cursor:
        yield Role(doc=r_doc)
            

def _get_role(role_c, role_id):
    '''
    获取指定role_id的Role对象
    '''
    return role_c.find_one({
        'role_id': role_id
        })
        

def _get_roles_without_disabled(role_c, *role_parent_ids):
    '''
    获取指定role_id序列中的所有未禁用的role文档
    '''
    return role_c.find({
            'role_id': {'$in': role_parent_ids},
            'disabled': {'$ne': True},
            })


def _get_roles_with_disabled(role_c, *role_parent_ids):
    '''
    获取指定role_id序列中的所有的role文档(包括已禁用的)
    '''
    return role_c.find({
            'role_id': {'$in': role_parent_ids},
            })


def role_add(role_name, role_desc, *role_parent_ids):
    '''
    添加角色
    '''
    role_c = db_hack.connect(collection=db_schema.ROLE) # 获取role集合
    try:
        if role_c.find_one({'name': role_name}) \
                is not None:
            # 角色名存在
            raise GeneralError(u'角色名称已存在')
        else:
            # 角色名称不存在, 添加该角色
            role_m = Role(role_name, description=role_desc)
            role_m.parent_roles = [] # 父级角色
            for p_role in \
                    _get_roles_without_disabled(role_c, *role_parent_ids):
                role_m.parent_roles.append(p_role['role_id'])

            # 若无父级角色, 删除该属性
            if len(role_m.parent_roles) <= 0: del role_m.parent_roles
                
            object_id = role_c.insert(role_m.get_doc())
            return Role(doc=role_c.find_one({'_id': object_id}))
    finally:
        del role_c # 释放集合


def role_remove(*role_ids):
    '''
    删除角色, 设置 disabled = True
    '''
    if role_ids is None:
        raise GeneralError(u"参数错误")
    role_c = db_hack.connect(collection=db_schema.ROLE)
    try:
        result = role_c.update(
            {'role_id': {'$in': role_ids}},
            {'$set': {
                    'disabled': True
                    }}
            )
        # result:
        # {u'updatedExisting': True, u'connectionId': 39, u'ok': 1.0, u'err': None, u'n': 1}
        # {u'updatedExisting': False, u'connectionId': 39, u'ok': 1.0, u'err': None, u'n': 0}
        return result['n'] # 返回更新数目
    finally:
        del role_c
