#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web

__metaclass__ = type

class StaticFile:
    def GET(self, file):
        raise web.seeother('/static/' + file)
