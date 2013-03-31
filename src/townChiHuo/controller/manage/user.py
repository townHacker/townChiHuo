#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
import web

from townChiHuo.util.mako_render import mako_render
from townChiHuo.util import mongodb_hack as db_hack
from townChiHuo.util import encrypt
from townChiHuo.settings import settings
import townChiHuo.models.model as model
import townChiHuo.models.user as user
from townChiHuo.models.error import GeneralError

class Index(object):
    def GET(self, *path):
        users = db_hack.connect(collection='users')
        u_iter = model.iter(users.find())
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/user/user.tmpl', users=u_iter)


class Add(object):
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/user/user_add.tmpl')

    def POST(self, *path):
        i = web.input('name', 'password', 'repassword')

        if i.password != i.repassword:
            result = dict( \
                isSucceed = False,
                msg = u'重复密码不一致')
        else:
            try:
                user.user_add(i.name, i.password)
                result = dict( \
                    isSucceed = True,
                    msg = u'添加成功')
            except GeneralError as err:
                result = dict( \
                    isSucceed = False,
                    msg = unicode(err.value))
                
        web.header('Content-Type', 'application/json')
        return json.dumps(result)

class Login(object):
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/user/login.tmpl')

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
        
