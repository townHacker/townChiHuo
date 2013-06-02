#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string, random, json, os, sys, uuid
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
            
            filename = form_data['upload_files'] \
                .filename \
                .replace('\\', '/').split('/')[-1]
            print '-- upload file: %s' % filename
            fout = open(
                os.path.join(settings.settings['UploadDir'], filename), 'wb')
            fout.write(form_data['upload_files'].file.read())
            
            return json.dumps(dict(
                isSucceed = True,
                file = u"/static_file/upload/%s" % unicode(filename, 'utf8'),))
        except Exception as e:
            print sys.exc_info()[0], e.args
            return json.dumps(dict(
                isSucceed = False,
                file = None,))



class ImageClip(object):
    def GET(self, *path):
        form_data = web.input('img_file', 'zoom', 'top', 'left', 'width', 'height')
        zoom, top, left, width, height = float(form_data['zoom']), \
                                         int(float(form_data['top'])), \
                                         int(float(form_data['left'])), \
                                         int(float(form_data['width'])), \
                                         int(float(form_data['height']))
        
        upload_dir = settings.settings['UploadDir']
        src_path = u"/static_file/upload/%s"
        img_path = os.path.join(upload_dir, form_data['img_file'])
        
        f_name = unicode(uuid.uuid4())
        f_name_200 = f_name + u'_200x200.png'
        f_name_100 = f_name + u'_100x100.png'
        f_name_50 = f_name + u'_50x50.png'

        result = {}
        if draw.figure_cut(img_path, zoom, top, left, width, height,
                           200, 200, os.path.join(upload_dir, f_name_200)):
            result['200x200'] = src_path % f_name_200
            
        if draw.figure_cut(img_path, zoom, top, left, width, height,
                           100, 100, os.path.join(upload_dir, f_name_100)):
            result['100x100'] = src_path % f_name_100

        if draw.figure_cut(img_path, zoom, top, left, width, height,
                           50, 50, os.path.join(upload_dir, f_name_50)):
            result['50x50'] = src_path % f_name_50
                
        return json.dumps(result)
                              

    def POST(self, *path):
        pass
