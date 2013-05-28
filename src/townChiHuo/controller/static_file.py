#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string, random, json, os
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


class FileUpload(object):
    '''
    上传文件
    '''
    def GET(self, file_name):
        
        ext = file_name.split('.')[-1]
        content_type = settings.content_type.get(ext)
        if content_type:
            web.header('Content-Type', content_type)
            web.header('Transfer-Encoding', 'chunked')
        fin = open(os.path.join(settings.settings['UploadDir'],
                                file_name), 'rb')
        try:
            rb = fin.read(1024)
            yield rb
            while rb:
                rb = fin.read(1024)
                yield rb
        finally:
            fin.close()

    
    def POST(self, *path):
        try:
            form_data = web.input(upload_files={},
                                  upload_success_script='',
                                  upload_fail_script='')
            print form_data
            filename = form_data['upload_files'] \
                .filename \
                .replace('\\', '/').split('/')[-1]
            
            fout = open(
                os.path.join(settings.settings['UploadDir'], filename), 'wb')
            fout.write(form_data['upload_files'].file.read())
            
            return u'<script type="text/javascript">%s</script>' \
                % 'top.window.upload_success_script("%s");' \
                % ("/static_file/upload/" + filename)
        except:
            return u'<script type="text/javascript">%s</script>' \
                % 'top.window.upload_fail_script();'


class ImageClip(object):
    def GET(self, *path):
        pass

    def POST(self, *path):
        pass
