#!/usr/bin/env python
# -*- coding: utf-8 -*-

# urls config

urls = (
    '/checkcode/?(.*)', 'controller.static_file.CheckCode',
    '/(?P<file>.*.css|.*.js|.*.jpg|.*.gif|.*.png|.*.ico)', 'controller.static_file.StaticFile',

    '/manage/login/?(.*)', 'controller.manage.user.Login', 
    '/manage/user_add/?(.*)', 'controller.manage.user.Add', 
    '/manage/delete/?(.*)','controller.manage.user.Delete',
    '/manage/user/?(.*)', 'controller.manage.user.Index',

    '/manage/action_permission/add/?(.*)', 'controller.manage.permission.AddActionPermission', 
    '/manage/action_permission/?(.*)', 'controller.manage.permission.ActionPermission',
    
    '/manage/role/delete/?(.*)', 'controller.manage.permission.DeleteRole', 
    '/manage/role/add/?(.*)', 'controller.manage.permission.AddRole', 
    '/manage/role/?(.*)', 'controller.manage.permission.Role',

    '/manage/permission/?(.*)', 'controller.manage.permission.Permission',

    '/manage/commodity_type/add/?(.*)', 'controller.manage.commodity.CommodityTypeAdd', 
    '/manage/commodity_type/?(.*)', 'controller.manage.commodity.CommodityType',
    '/manage/commodity/?(.*)', 'controller.manage.commodity.Commodity',
        
    '/manage/?(.*)', 'controller.manage.index.Index',
	
    #'/login/?(.*)', 'controller.index.Login',
    '/register/?(.*)', 'controller.index.Register',
    
    '/(.*)', 'controller.index.Index',
)
