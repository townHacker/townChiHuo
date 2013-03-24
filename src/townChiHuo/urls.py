#!/usr/bin/env python
# -*- coding: utf-8 -*-

# urls config

urls = (
    '/checkcode/?(.*)', 'controller.static_file.CheckCode',
    '/(?P<file>.*.css|.*.jpg|.*.gif|.*.png)', 'controller.static_file.StaticFile',
    
    '/manage/user_add/?(.*)', 'controller.manage.user.Add', 
    '/manage/user/?(.*)', 'controller.manage.user.Index',
    '/manage/action_permission/?(.*)', 'controller.manage.permission.ActionPermission', 
    '/manage/permission/?(.*)', 'controller.manage.permission.Permission',
    '/manage/?(.*)', 'controller.manage.index.Index',
    
    '/login/?(.*)', 'controller.index.Login',
    '/register/?(.*)', 'controller.index.Register',
    
    '/(.*)', 'controller.index.Index',
)
