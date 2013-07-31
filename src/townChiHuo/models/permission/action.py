#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import uuid

from mongoengine import *

from townChiHuo.models.error import GeneralError
from townChiHuo.models.permission.role import Role
import townChiHuo.db_schema as db_schema
from townChiHuo.util import mongodb_hack as db_hack
from townChiHuo.models.permission.permission import RolePermission


class Action(Document):
    '''
    action 动作
    action_id: action id
    action_name: action 名称
    action_code: action 代码
    default_permission: 默认权限
    permissions: 权限 -- list of { role_id, permission_code }
    '''
    action_id = StringField(required=True, unique=True,
                          default=unicode(uuid.uuid4()))
    action_name = StringField(max_length=200, required=True)
    action_code = StringField()
    default_permission = IntField()
    permissions = ListField(EmbeddedDocumentField(RolePermission), default=[])

    meta = { 'collection': db_schema.ACTION }

    
    def add_permission(self, *role_permission_args):
        '''
        添加action的权限设置
        '''
        if not self.permissions:
            self.permissions = []
        if not len(role_permission_args):
            return

        # 构建新的action权限数据
        new_permissions = []
        for perm in itertools.dropwhile( \
            lambda x:x.role.id in \
                [ a.role.id for a in role_permission_args], \
                    self.permissions):
            new_permissions.append(perm)

        new_permissions[len(self.permissions):] \
            = role_permission_args

        self.permissions = new_permissions

        self.save()
        self.reload()
        



    def get_permissions(self):
        '''
        获取指定action的所有权限设置
        '''
        def get_role_name(role_c, role_id):
            return role_c.find_one({'id': role_id})['name']
        
        action_c = Action._get_collection()
        role_c = Role._get_collection()
        try:
            all_act = action_c.aggregate([
                {"$match": {
                    'id': self.id
                }}, 
                {"$unwind": "$permissions"},
                {"$project": {
                    'id': 1,
                    'action_name': 1,
                    'default_permission': 1,
                    'role_id': '$permissions.role.id',
                    'permission_code': '$permissions.permission_code', 
                }},
            ])


            for a_item in all_act['result']:
                a_item['role_name'] = get_role_name(role_c, a_item['role_id'])

            return all_act['result']
        finally:
            del action_c
            del role_c


            

