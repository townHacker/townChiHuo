#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import web

try:
    import pylibmc as memcache
except ImportError:
    import memcache

sys.path.append(os.path.dirname( \
        os.path.dirname(os.path.abspath(sys.argv[0]))))

import townChiHuo

from townChiHuo.urls import urls
from townChiHuo.util import session
from townChiHuo import settings
from townChiHuo.controller import index


if __name__ == '__main__':
    
    app = web.application(urls, globals())

    # use memcached for session store
    mc = memcache.Client(settings.settings['memcached.hosts'])
    mc_store = session.MemcachedStore(mc)

    session = web.session.Session(app, mc_store, initializer={})

    def session_hook():
        web.ctx.session = session

    # 添加session处理
    app.add_processor(web.loadhook(session_hook))

    # print
    print sys.prefix
    print urls
    print sys.path
    print web.ctx
    print settings.action_auth
    
    app.run()
