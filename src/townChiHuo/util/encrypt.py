#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

def md5(password, key):
    '''
    生成md5加密后的密码，返回加密后的密码
    '''
    m = hashlib.md5()
    m.update(key + password)
    return m.hexdigest()


if __name__ == '__main__':
    import sys
    print unicode(md5('123', 'abc'))
    print unicode(md5('123', 'abc'), errors='replace')
    print sys.getdefaultencoding()
    print sys.getfilesystemencoding()
    import locale
    print locale.getdefaultlocale()
    print locale.getpreferredencoding()
