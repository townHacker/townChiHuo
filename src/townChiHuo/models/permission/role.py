#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from townChiHuo.models import model
from townChiHuo.models.error import GeneralError

import townChiHuo.db_schema as db_schema


class Role(model.Model):
    '''
    角色
    role_id # 角色id
    name # 角色名称
    description # 角色描述
    parent_roles # 父级角色
    '''
    role_id = None
    name = None
    def __init__(self, name, role_id=None, description=None, doc=None):
        if role_id is None:
            role_id = uuid.uuid4()
        self.role_id = role_id
        self.name = name
        self.description = description
        super(Role, self).__init__(doc=doc)
        

def get_roles(role_c, *role_parent_ids):
    '''
    获取指定role_id序列中的所有未禁用的role文档
    '''
    return role_c.find({
            'role_id': {'$in': role_parent_ids},
            'disabled': {'$ne': True},
            })


def get_all_roles(role_c, *role_parent_ids):
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
    role_c =  db_hack.connect(collection=db_schema.ROLE) # 获取role集合
    try:
        if role_c.find_one({'name': role_name}) \
                is not None:
            # 角色名存在
            raise GeneralError(u'角色名称已存在')
        else:
            # 角色名称不存在, 添加该角色
            role_m = Role(role_name, description=role_desc)
            role_m.parent_roles = [] # 父级角色
            for p_role in get_roles(role_c, *role_parent_ids):
                role.parent_roles.append(p_role.role_id)

            # 若无父级角色, 删除该属性
            if role_m.parent_roles.count() <= 0: del role_m.parent_roles
                
            object_id = role_c.insert(role_m.get_doc())
            return Role(doc=role_c.find_one({'_id': object_id}))
    finally:
        del role_c # 释放集合

        
