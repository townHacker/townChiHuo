#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

import json
import web

from townChiHuo.util.mako_render import mako_render
from townChiHuo.util import mongodb_hack as db_hack
import townChiHuo.models.model as model
import townChiHuo.models.user as user
from townChiHuo.models.error import GeneralError

class Index:
    def GET(self, *path):
        users = db_hack.connect(collection='users')
        u_iter = model.iter(users.find())
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/user.tmpl', users=u_iter)


class Add:
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/user_add.tmpl')

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
