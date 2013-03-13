#!/usr/bin/env python
# -*- coding: utf-8 -*-

# urls config

urls = (
    '/(?P<file>.*.css|.*.jpg)', 'controller.static_file.StaticFile',
    '/manage/(.*)', 'controller.manage_index.Index',
    '/login/?(.*)', 'controller.index.Login',
    '/register/?(.*)', 'controller.index.Register',
    '/(.*)', 'controller.index.Index',
)
