#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

import web

from townChiHuo.util.mako_render import mako_render
from townChiHuo.util.decorator import action_auth_decorator
from townChiHuo.settings import action_auth
from townChiHuo.models.permission import permission
from townChiHuo.models.permission import role

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
        return mako_render('/manage/permission/permission.tmpl')

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
        return mako_render('/manage/permission/action_permission.tmpl', actions=actions)


class Role(object):
    def GET(self, *path):
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/permission/role.tmpl')


class AddRole(object):
    '''
    添加角色
    '''
    def POST(self, *path):
        try :
            i = web.input('role_name', role_desc=None, role_parent_ids=[])
            new_role = role.role_add(role_name=i.role_name, \
                                         role_desc=i.role_desc, \
                                         *i.role_parent_ids)
            result = dict(
                isSucceed= True,
                msg= u"添加角色成功",
                )
        except GeneralError as e:
            result = dict(
                isSucceed = False,
                msg = e.value,
                )
        web.header('Content-Type', 'application/json')
        return json.dumps(result)
            
            
class DeleteRole(object):
    '''
    删除角色
    '''
    def POST(self, *path):
        try :
            i = web.input('role_id')
            d_num = role.role_remove(i.role_id)
            result = dict(
                isSucceed = True,
                msg = u"成功删除{:d}个角色".format(d_num),
                )
        except GeneralError as err:
            result = dict(
                isSucceed = False,
                msg = err.value,
                )
        web.header('Content-Type', 'application/json')
        return json.dumps(result)
        
