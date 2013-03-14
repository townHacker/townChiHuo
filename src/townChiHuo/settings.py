#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TemplateLookupDir : mako TemplateLookup 的寻找模板目录
# MakoModuleDir :　mako module 缓存的目录

import os

#root_dir = sys.path[0]
root_dir = os.path.dirname(os.path.abspath(__file__))

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
    'font': os.path.join(root_dir, 'static/fonts/wqy-zenhei.ttc'),
}

if __name__ == '__main__':
    import sys
    print 'sys.path : ', sys.path
    print 'sys.prefix: ', sys.prefix
    print 'settings: ', settings
