#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

import web

from mako_render import mako_render

class Index:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage_index/index.tmpl')

