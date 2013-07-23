#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index controller actions

import web

from townChiHuo.settings import settings
from townChiHuo.util.mako_render import mako_render
from townChiHuo.models import user
from townChiHuo.models.error import *
from townChiHuo.util.decorator import action_auth_decorator
from townChiHuo.models.permission import permission

# 15
_def_permission = 0 \
    | permission.READABLE \
    | permission.EDITABLE \
    | permission.DELETABLE \
    | permission.EXECUTABLE

class Index:
    @action_auth_decorator(action_id=u'decd4c09-148c-4b30-a58a-74bf5b3aa8f6', \
                               action_name=u'首页页面', \
                               action_code=u'index.Index.GET', \
                               default_permission=_def_permission)
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/index/index.tmpl')


class Register:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/index/register.tmpl')
    
    def POST(self, *path):
        web.header('Content-Type', 'text/plain')
        
        i = web.input('email', 'password', 're_password')
        try: 
            user_new = user.register(email=i.email, \
                                     password=i.password)
        except GeneralError as e:
            return e.value
    
        return u'注册成功'

    
class Login:
    @action_auth_decorator(action_id=u'd9620d01-3bc8-4068-be8a-7097d340bcb2', \
                               action_name=u'登录页面', \
                               action_code=u'index.Login.GET', \
                               default_permission=_def_permission)
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        action_name = self.GET.get_action_name()
        action_id = self.GET.get_action_id()
        action_code = self.GET.get_action_code()
        permission = self.GET.get_default_permission()
        return mako_render('/index/login.tmpl')

    @action_auth_decorator(action_id=u'7b969732-eb44-427a-8bb9-88c7665d7993', \
                               action_name=u'登录请求', \
                               action_code=u'index.Login.POST', \
                               default_permission=_def_permission)
    def POST(self, *path):
        web.header('Content-Type', 'text/plain')
        i = web.input()
        result = user.login(u_name=i.name, \
                                password=i.password)
        if result[0]:
            u = result[1]
            session = web.ctx.session
            session['login_user'] = u
            return u'登录成功'
        else:
            return u'登录失败'


class Commodity:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/index/commodity.tmpl')
