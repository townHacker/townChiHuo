#!/usr/bin/env python
# -*- coding: utf-8 -*-

# index controller actions

from mako.template import Template

class index:
    def GET(self):
        # change the filename with your local index.tmpl file absolute path
        template = Template(filename="/home/bamboo/townChiHuo/src/template/index/index.tmpl")
        return template.render(content="here is content!!!")
