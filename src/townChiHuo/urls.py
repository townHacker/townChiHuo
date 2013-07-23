#!/usr/bin/env python
# -*- coding: utf-8 -*-

def extend_tuple(tuple1, tuple2):
    if isinstance(tuple1, tuple) and isinstance(tuple2, tuple):
        target = list(tuple1)
        target.extend(list(tuple2))
        return tuple(target)

# urls config

global_urls = (
    '/static_file/imageclip/?(.*)', 'controller.static_file.ImageClip',
    '/static_file/upload/?(?P<file_name>.*)', 'controller.static_file.FileUpload', 
    '/checkcode/?(.*)', 'controller.static_file.CheckCode',
    '/(?P<file>.*.css|.*.js|.*.jpg|.*.gif|.*.png|.*.ico)', 'controller.static_file.StaticFile',
    
)

front_urls = (
    
    #'/login/?(.*)', 'controller.index.Login',
    '/register/?(.*)', 'controller.index.Register',

    '/commodity/?(.*)', 'controller.index.Commodity', 
    
    '/(.*)', 'controller.index.Index',
    )
front_urls = extend_tuple(global_urls, front_urls)


manage_urls = (
    
    '/login/?(.*)', 'controller.manage.user.Login',
    '/logout/?(.*)', 'controller.manage.user.Logout',
    
    '/user_add/?(.*)', 'controller.manage.user.Add', 
    '/delete/?(.*)','controller.manage.user.Delete',
    '/user/?(.*)', 'controller.manage.user.Index',

    '/action_permission/add/?(.*)', 'controller.manage.permission.AddActionPermission', 
    '/action_permission/?(.*)', 'controller.manage.permission.ActionPermission',
    
    '/role/delete/?(.*)', 'controller.manage.permission.DeleteRole', 
    '/role/add/?(.*)', 'controller.manage.permission.AddRole', 
    '/role/?(.*)', 'controller.manage.permission.Role',

    '/permission/?(.*)', 'controller.manage.permission.Permission',


    '/commodity_type/add/?(.*)', 'controller.manage.commodity.CommodityTypeAdd', 
    '/commodity_type/?(.*)', 'controller.manage.commodity.CommodityType',
    '/commodity/add/?(.*)', 'controller.manage.commodity.CommodityAdd', 
    '/commodity/?(.*)', 'controller.manage.commodity.Commodity',
        
    '/?(.*)', 'controller.manage.index.Index',
    )
manage_urls = extend_tuple(global_urls, manage_urls)


if __name__ == '__main__':
    print 'global_urls: ', global_urls, '\r\n'
    print 'front_urls: ', front_urls, '\r\n'
    print 'manage_urls: ', manage_urls, '\r\n'
