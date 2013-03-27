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
        return mako_render('/manage/index.tmpl', curr_user=curr_user)

class Login(object):
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/login.tmpl')

    def POST(self, *path):
        i = web.input('name', 'password', 'checkcode')
        try:
            s = web.ctx.session # 获取session

            if 'code_ref' not in s:
                raise GeneralError(u"验证码失效")
                
            code_ref = s['code_ref'] # 获取 验证码md5
            cc = i.checkcode.lower()
            if code_ref != encrypt.md5(cc, settings["checkcode.md5key"]):
                raise GeneralError(u"验证码错误")
            
            curr_user = user.login(u_name=i.name, \
                                       password=i.password)

            s['curr_user'] = curr_user # session中保存当前用户
            del s['code_ref'] # 删除验证码
            result = dict(
                isSucceed = True,
                msg = '登录成功'
                )
        except GeneralError as e:
            result = dict(
                isSucceed = False, 
                msg = e.value
                )
        web.header('Content-Type', 'application/json')
        return json.dumps(result)
        
