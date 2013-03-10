#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index controller actions


from settings import settings
from mako_render import mako_render

import web

class index:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('index/index.tmpl', content='here is content!!!')


