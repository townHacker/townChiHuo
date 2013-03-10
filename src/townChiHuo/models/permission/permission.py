#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

class permission:
    '''
    权限许可
    '''
    permission_code = 0 # 许可码
    def __init__(self, permission_code=0):
        self.permission_code = permission_code


class readable_permission:
    '''
    可读权限
    '''
    read_mask = 0x01 # 读 掩码

class editable_permission:
    '''
    可编辑权限
    '''
    edit_mask = 0x02 # 写 掩码

class deletable_permission:
    '''
    可删除权限
    '''
    delete_mask = 0x04 # 删 掩码

class executable_permission:
    '''
    可执行权限
    '''
    execute_mask = 0x08 # 执行 掩码
    
class permisssion_group:
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
