#!/usr/bin/env python
# -*- coding: utf-8 -*-

#login controller actions


from settings import settings
from mako_render import mako_render

import web

class login:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('login/login.tmpl')
    



