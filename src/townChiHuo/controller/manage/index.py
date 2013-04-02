#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import web

from townChiHuo.util.mako_render import mako_render
from townChiHuo.util import mongodb_hack as db_hack
import townChiHuo.util.encrypt as encrypt
from townChiHuo.settings import settings
from townChiHuo.models import user
from townChiHuo.models.error import *

class Index(object):
    def GET(self, *path):
        s = web.ctx.session
        if "curr_user" not in s:
            raise web.seeother('/manage/login')
        curr_user = s['curr_user']
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/index.tmpl')


