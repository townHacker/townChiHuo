#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

import web

from townChiHuo.util.mako_render import mako_render

class Index:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/index.tmpl')

