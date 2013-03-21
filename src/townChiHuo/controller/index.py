#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index controller actions

import web

from townChiHuo.settings import settings
from townChiHuo.util.mako_render import mako_render
from townChiHuo.models import user

class Index:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('index/index.tmpl')


class Register:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('index/register.tmpl')
    
    def POST(self, *path):
        web.header('Content-Type', 'text/plain')
        
        i = web.input('email', 'password', 're_password')
        try: 
            user_new = user.register(email=i.email, \
                                     password=i.password)
        except Exception as e:
            return e[0]
    
        return u'注册成功'

    
class Login:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('index/login.tmpl')
    
    def POST(self, *path):
        web.header('Content-Type', 'text/plain')
        i = web.input()
        result = user.login(u_name=i.name, \
                                password=i.password)
        if result:
            return u'登录成功'
        else:
            return u'登录失败'
