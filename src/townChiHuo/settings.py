#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TemplateLookupDir : mako TemplateLookup 的寻找模板目录
# MakoModuleDir :　mako module 缓存的目录

import sys
import os

root_dir = sys.path[0]

settings = {
    "RootDir": root_dir,
    "TemplateLookupDir": [
        os.path.join(root_dir, "template")
        ],
    "MakoModuleDir": os.path.join(root_dir, "mako_module"), 
}

if __name__ == '__main__':
    print 'sys.path : ', sys.path
    print 'sys.prefix: ', sys.prefix
    print 'settings: ', settings
