#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string, random
import web

from townChiHuo.util import draw, encrypt
from townChiHuo import settings

__metaclass__ = type

class StaticFile:
    def GET(self, file):
        raise web.seeother('/static/' + file)

class CheckCode:
    def GET(self, *path):
        def get_val():
            all_char = string.letters + string.digits
            val = ''
            for i in range(4):
                val += all_char[random.randint(0, len(all_char)-1)]
            return val

        s = get_val()
        web.header('Content-Type', 'image/png')
        ecode = encrypt.md5(s.lower(), settings.settings['checkcode.md5key'])
#        web.header('code_ref', ecode)

        session = web.ctx.session
        session['code_ref'] = ecode
        
        return draw.check_code(s, font_file=settings.settings['font'])
