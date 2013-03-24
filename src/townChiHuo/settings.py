#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TemplateLookupDir : mako TemplateLookup 的寻找模板目录
# MakoModuleDir :　mako module 缓存的目录

import os
import sys

root_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

settings = {
    "RootDir": root_dir,
    "TemplateLookupDir": [
        os.path.join(root_dir, "template")
        ],
    "MakoModuleDir": os.path.join(root_dir, "mako_module"),

    # mongodb setting
    'mongodb.host': 'localhost',
    'mongodb.port': 27017,
    'mongodb.db': 'townChiHuo',

    # md5加密
    'password.md5key': '704f8303-85e5-4eac-ab54-49d7f301500e',
    'checkcode.md5key': '0841f736-58cc-42e3-bf87-7bc21f08f963',

    # 字体
    'font': os.path.join(root_dir, 'static/fonts/TSCu_Comic.ttf'),

    # memcached
    'memcached.hosts': [
        '127.0.0.1:11211'
        ]
}

# 数据库集合
db_schema = dict(
    USER = 'users', # 用户集合
    ROLE = 'roles', # 角色集合
)

# Action 认证
action_auth = dict()

if __name__ == '__main__':
    import sys
    print 'sys.path : ', sys.path
    print 'sys.prefix: ', sys.prefix
    print 'settings: ', settings
