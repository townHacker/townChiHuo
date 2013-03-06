#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index controller actions

import sys

from settings import settings
from mako_render import mako_render

class index:
    def GET(self):
        return mako_render('index/index.tmpl', content='here is content!!!')
#        return settings['TemplateLookupDir']

