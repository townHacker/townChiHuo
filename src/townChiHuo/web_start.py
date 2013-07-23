#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import web

try:
    import pylibmc as memcache
except ImportError:
    import memcache

#print sys.argv[0]
#print __file__

# __file__   # sys.argv[0]
#sys.path.append(os.path.dirname( \
#        os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.curdir)))

#print sys.path

import townChiHuo

import townChiHuo.urls as urls
from townChiHuo.util import session
from townChiHuo import settings
from townChiHuo.controller import index



# check upload directory
upload_dir = settings.settings['UploadDir']
if not os.path.exists(upload_dir):
    print 'create directory: ', upload_dir
    os.makedirs(upload_dir)

manage_app = web.application(urls.manage_urls, globals())

front_app = web.application(
    urls.extend_tuple(( '/manage', manage_app, ), 
                      urls.front_urls), globals())

# use memcached for session store
mc = memcache.Client(settings.settings['memcached.hosts'])

print 'clear all sessions...'
mc.flush_all()

mc_store = session.MemcachedStore(mc)

session = web.session.Session(front_app, mc_store, initializer={'count': 0})


def session_hook():
    web.ctx.session = session

# 添加session处理
front_app.add_processor(web.loadhook(session_hook))


# web.py web.config.debug=False 配置web.py的调试功能
if settings.settings['web.config.debug'].lower() != 'true':
    web.config.debug = False
else:
    web.config.debug = True

print 'web.config.debug(web.py 调试功能): ', web.config.debug


# print sys.prefix
# print urls
# print sys.path
# print web.ctx
# print settings.action_auth
application = front_app.wsgifunc()

if __name__ == '__main__':
    print "Running ..."
    front_app.run()
