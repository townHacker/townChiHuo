#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string, random, json
import web

from townChiHuo.util import draw, encrypt
from townChiHuo import settings


class StaticFile(object):
    def GET(self, file):
        raise web.seeother('/static/' + file)

class CheckCode(object):
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


class UploadFile(object):
    '''
    上传文件
    '''
    def GET(self, *path):
        pass
    
    def POST(self, *path):
        
        form_data = web.input(upload_files={})
        if not form_data.upload_files:
            return json.dumps({ 'msg' : 'failed' })
        else:
            filename = form_data['upload_files'].file_name \
                .replace('\\', '/').split('/')[-1]

            import os
            fout = open(os.path.join(settings['UploadDir'], filename), 'w')
            fout.write(form_data['upload_files'].file.read())

            return json.dumps({ 'msg' : 'successful' })
