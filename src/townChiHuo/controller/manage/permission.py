#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

from townChiHuo.util.mako_render import mako_render
from townChiHuo.util.decorator import action_auth_decorator
from townChiHuo.settings import action_auth
from townChiHuo.models.permission import permission

_def_permission = 0 \
    | permission.READABLE \
    | permission.EDITABLE \
    | permission.DELETABLE \
    | permission.EXECUTABLE

class Permission(object):
    @action_auth_decorator(action_id=u'cb9dc21e-8eb7-421d-a166-7045b46ed8e2', \
                               action_name=u'权限管理页面', \
                               action_code=u'permission.Permission.GET', \
                               default_permission=_def_permission)
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/permission.tmpl')

class ActionPermission(object):
    @action_auth_decorator(action_id=u'9adcbdb0-10ac-4870-949e-8dddcd4c9413', \
                               action_name=u'Action权限管理页面', \
                               action_code=u'permission.ActionPermission.GET', \
                               default_permission=_def_permission)
    def GET(self, *path):
        def get_action():
            for k, v in action_auth.iteritems():
                yield v

        actions = get_action()

        web.header('Content-Type', 'text/html')
        return mako_render('/manage/action_permission.tmpl', actions=actions)
