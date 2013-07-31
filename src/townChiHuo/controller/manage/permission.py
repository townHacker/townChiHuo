#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import web

from pymongo.bson.objectid import ObjectId

from townChiHuo.util.mako_render import mako_render
from townChiHuo.util.decorator import action_auth_decorator
from townChiHuo.settings import action_auth
from townChiHuo.models.permission import permission
from townChiHuo.models.permission import role
from townChiHuo.models.permission import action
from townChiHuo.models.error import GeneralError

def get_action():
    for k, v in action_auth.iteritems():
        yield v


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
        all_roles = role.get_roles()

        all_actions = get_action()

        all_perm = []
        for a_item in get_action():
            all_perm[len(all_perm):] = \
                list(a_item.get_permissions())
        
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/permission/permission.tmpl', \
                               roles=all_roles, \
                               actions=all_actions, \
                               permissions=all_perm)


class ActionPermission(object):
    @action_auth_decorator(action_id=u'9adcbdb0-10ac-4870-949e-8dddcd4c9413', \
                               action_name=u'Action权限管理页面', \
                               action_code=u'permission.ActionPermission.GET', \
                               default_permission=_def_permission)
    def GET(self, *path):

        actions = get_action()

        web.header('Content-Type', 'text/html')
        return mako_render('/manage/permission/action_permission.tmpl', \
                actions=actions)

class AddActionPermission(object):
    
    def POST(self, *path):

        def calc_code(*permission_code):
            sum = 0
            for item_c in permission_code:
                sum |= int(item_c)
            return sum

        try:
            i = web.input(permission_role=[],
                          permission_action=[],
                          permission_code=[])

            if not i.permission_role:
                raise GeneralError(u'请选择角色')
            if not i.permission_action:
                raise GeneralError(u'请选择Action')
            
            p_code = calc_code(*i.permission_code)
            for a_item in i.permission_action:
                permissions = []
                for r_item in i.permission_role:
                    permissions.append(permission.RolePermission(
                        role=role.Role.objects(id=ObjectId(r_item)).first(),
                        permission_code=p_code))
                    
                action.Action.objects(id=ObjectId(a_item)).first() \
                    .add_permission(*permissions)

            result = dict(
                isSucceed = True,
                msg = '添加成功',
                )
        except GeneralError as err:
            result = dict(
                isSucceed = False,
                msg = err.value,
                )
        web.header('Content-Type', 'application/json')
        return json.dumps(result)


class Role(object):
    def GET(self, *path):
        i = web.input(page=0, size=10) 
        i.page, i.size = int(i.page), int(i.size)
        count = role.get_roles_count()
        import math
        page_count = int(math.ceil(float(count) / i.size)) 

        i.page = i.page if i.page > 0 else 0
        i.page = i.page if i.page < page_count \
                 else max(page_count-1, 0)

        limit, skip = i.size, i.page * i.size
        a_roles = role.get_roles(limit=limit, skip=skip)
        all_roles = role.get_roles()
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/permission/role.tmpl', \
                               roles=a_roles, \
                               all_roles=all_roles, \
                               page_count=max(page_count, 1), \
                               page=i.page)


class EditRole(object):
    '''
    编辑角色
    '''
    def GET(self, *path):
        pass

    def POST(self, *path):
        pass


class AddRole(object):
    '''
    添加角色
    '''
    @action_auth_decorator(action_id=u'bc0ae985-43af-4a29-aec2-5edba5384e3d', \
                               action_name=u'角色添加', \
                               action_code=u'permission.AddRole.POST', \
                               default_permission=_def_permission)
    def POST(self, *path):
        try :
            i = web.input('role_name', role_desc=None, parent_role=[])
            print i.role_desc
            new_role = role.role_add(i.role_name, \
                                     i.role_desc, \
                                     *i.parent_role)
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
    @action_auth_decorator(action_id=u'd5ea0a06-a531-4301-ac2d-41083a62403b', \
                               action_name=u'角色删除', \
                               action_code=u'permission.DeleteRole.GET', \
                               default_permission=_def_permission)
    def GET(self, *path):
        try :
            i = web.input('role_id')
            d_num = role.role_remove(ObjectId(i.role_id))
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
        
