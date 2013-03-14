#!/usr/bin/env python
# -*- coding: utf-8 -*-

# some helper method for mako render
# use mako.lookup.TemplateLookup

from mako.template import Template
from mako.lookup import TemplateLookup
from settings import settings

tmplLookup = TemplateLookup(directories=settings['TemplateLookupDir'], \
                       module_directory=settings['MakoModuleDir'], \
                                default_filters=['decode.utf8'], \
                                input_encoding='utf-8', \
                                output_encoding='utf-8')

def mako_render(tmpl_name, **args):
    tmpl = tmplLookup.get_template(tmpl_name)
#    return tmpl.render(**args)
    return tmpl.render_unicode(**args).encode('utf-8', 'replace')

if __name__ == '__main__':
    print mako_render('index/index.tmpl', content='abc')
