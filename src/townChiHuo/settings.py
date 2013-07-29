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
    "UploadDir": os.path.join(root_dir, "upload-files"),

    # mongodb setting
    'mongodb.host': 'localhost',
    'mongodb.port': 27017,
    'mongodb.db': 'benpig',

    # md5加密
    'password.md5key': '704f8303-85e5-4eac-ab54-49d7f301500e',
    'checkcode.md5key': '0841f736-58cc-42e3-bf87-7bc21f08f963',

    # 字体
    'font': os.path.join(root_dir, 'static/fonts/TSCu_Comic.ttf'),

    # memcached
    'memcached.hosts': [
        '127.0.0.1:11211'
        ],

    # web.py config
    'web.config.debug': 'True', 
}

# Action 认证
action_auth = dict()


# file extension to http content type
content_type = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'ico': 'image/x-icon',
    'txt': 'application/octet-stream',
}

if __name__ == '__main__':
    import sys
    print 'sys.path : ', sys.path
    print 'sys.prefix: ', sys.prefix
    print 'settings: ', settings
