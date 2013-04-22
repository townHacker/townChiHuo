#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from townChiHuo.util.mako_render import mako_render

class Commodity(object):

    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/commodity.tmpl')
