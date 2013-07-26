#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mongoengine import *

from townChiHuo.model.permission.role import Role


READABLE = 0x01 # 可读
EDITABLE = 0x02 # 可写(编辑)
DELETABLE = 0x04 # 可删
EXECUTABLE = 0x08 # 可执行

__all_permission = READABLE \
    | EDITABLE \
    | DELETABLE \
    | EXECUTABLE


def set_readable(permission_code):
    '''
    设置可读
    '''
    return permission_code | READABLE

def set_editable(permission_code):
    '''
    设置可写(编辑)
    '''
    return permission_code | EDITABLE

def set_deletable(permission_code):
    '''
    设置可删除
    '''
    return permission_code | DELETABLE
    
def set_executable(permission_code):
    '''
    设置可执行
    '''
    return permission_code | EXECUTABLE

def is_readable(permission_code):
    '''
    判断是否可读
    '''
    return bool(permission_code & READABLE)

def is_editable(permission_code):
    '''
    判断是否可写
    '''
    return bool(permission_code & EDITABLE)

def is_deletable(permission_code):
    '''
    判断是否可删除
    '''
    return bool(permission_code & DELETABLE)

def is_executable(permission_code):
    '''
    判断是否可执行
    '''
    return bool(permission_code & EXECUTABLE)

class Permission(EmbeddedDocument):
    '''
    权限
    resource: 权限针对的资源
    permission_code: 权限码
    target: 权限限制的目标
    '''
    

class RolePermission(EmbeddedDocument):
    '''
    角色权限
    '''
    role = ReferenceField(Role)
    permission_code = IntField()

class PermisssionGroup(object):
    '''
    权限组
    '''
    permissions = []
    length = 0
    def __init__(self, permissions = [], length = None):
        '''
        初始化权限组，可使用权限列表，length可指定权限组的大小
        '''
        self.permissions = permissions
        self.length = len(self.permissions)

        if length is not None:
            self.length = length
            if actual_len < length:
                self.permissions[self.length:] \
                    = [None] * (length - self.length)

        
    def add(self, permission, group_index):
        '''
        向权限组中添加一个权限，若组元素个数小于索引，则增大权限组，以添加权限
        '''
        if group_index >= self.length:
            self.permissions[self.length:] \
                = [None] * (group_index - self.length + 1)
            
        self.permissions[group_index] = permission

    def remove(self, group_index):
        '''
        删除指定索引的权限，即将该索引位置为None
        '''
        if self.length <= group_index:
            # 若列表不存在指定索引
            return
        self.permissions[group_index] = None

