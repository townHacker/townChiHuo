#!/usr/bin/env python
# -*- coding: utf-8 -*-

# urls config

urls = (
    '/checkcode/?(.*)', 'controller.static_file.CheckCode',
    '/(?P<file>.*.css|.*.jpg|.*.gif|.*.png)', 'controller.static_file.StaticFile',
    '/manage/(.*)', 'controller.manage_index.Index',
    '/login/?(.*)', 'controller.index.Login',
    '/register/?(.*)', 'controller.index.Register',
    '/(.*)', 'controller.index.Index',
)
