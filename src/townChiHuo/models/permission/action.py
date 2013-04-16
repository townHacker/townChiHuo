#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

import townChiHuo.models.model as model
from townChiHuo.models.error import GeneralError
from townChiHuo.models.permission.role import Role
import townChiHuo.db_schema as db_schema
from townChiHuo.util import mongodb_hack as db_hack

class Action(model.Model):
    '''
    action 动作
    action_id: action id
    action_name: action 名称
    action_code: action 代码
    default_permission: 默认权限
    permissions: 权限 -- tuple of { role_id, permission_code }
    '''
    def __init__(self, doc=None):
        super(Action, self).__init__(doc=doc)


def add_permission(action_id, *role_permission_args):
    '''
    添加action的权限设置
    '''
    action_c = db_hack.connect(collection=db_schema.ACTION) # 获取action集合
    try:
        action_doc = action_c.find_one({'action_id': action_id})
        if action_doc:
            if not action_doc.get('permissions'):
                action_doc['permissions'] = []

            if not len(role_permission_args):
                return

            # 构建新的 action 的权限数组
            new_permissions = []
            for perm in itertools.dropwhile( \
                lambda x:x['role_id'] in \
                    [a['role_id'] for a in role_permission_args], \
                    action_doc['permissions']):
                new_permissions.append(perm)
                
            new_permissions[len(action_doc['permissions']):] \
                = role_permission_args

            action_doc['permissions'] = new_permissions

            action_c.save(action_doc)
        else:
            raise GeneralError(u'指定的action_id不存在')
    finally:
        del action_c


def get_permissions(action_id):
    '''
    获取指定action的所有权限设置
    '''
    def get_role_name(role_c, role_id):
        return role_c.find_one({'role_id': role_id})['name']
        
    action_c = db_hack.connect(collection=db_schema.ACTION)
    role_c = db_hack.connect(collection=db_schema.ROLE)
    try:
        all_act = action_c.aggregate([
                {"$match": {
                        'action_id': action_id
                        }}, 
                {"$unwind": "$permissions"},
                {"$project": {
                        'action_id': 1,
                        'action_name': 1,
                        'default_permission': 1,
                        'role_id': '$permissions.role_id',
                        'permission_code': '$permissions.permission_code', 
                        }},
                ])


        for a_item in all_act['result']:
            a_item['role_name'] = get_role_name(role_c, a_item['role_id'])

        return all_act['result']
    finally:
        del action_c
        del role_c


            

