#!/usr/bin/env python
# -*- coding: utf-8 -*-

# some helper method for mako render
# use mako.lookup.TemplateLookup

from mako.template import Template
from mako.lookup import TemplateLookup
from settings import settings

#tmplLookup = TemplateLookup(directories=settings['TemplateLookupDir'], \
#                       module_directory=['MakoModuleDir'])
tmplLookup = TemplateLookup(directories=settings['TemplateLookupDir'])
def mako_render(tmpl_name, **args):
    tmpl = tmplLookup.get_template(tmpl_name)
    return tmpl.render(**args)

if __name__ == '__main__':
    print mako_render('index/index.tmpl', content='abc')
