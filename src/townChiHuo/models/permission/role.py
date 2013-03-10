#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

import uuid


class role:
    '''
    角色
    '''
    role_id = None
    name = None
    def __init__(self, name, role_id=None):
        if role_id is None:
            role_id = uuid.uuid4()
        self.role_id = role_id
        self.name = name
        
