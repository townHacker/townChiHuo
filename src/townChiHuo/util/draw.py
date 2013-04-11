#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Image, ImageDraw, ImageFont
import itertools
import StringIO

def check_code(val, len=4, fmt='PNG', size=(98, 36), font_file=None):
    '''
    画图工具，得到指定字符串的验证码图片
    font_file: 指定字体文件。请使用.ttf/.ttc字体
    '''
    def region():
        x = size[0] / len
        y = size[1]
        for i in range(len):
            yield (2+x*i, 2, 2+x*(i+1), y-2)
            
    val = val[0:len]
    if font_file:
        font = ImageFont.truetype(font_file, 30, encoding="unic")
    else :
        font = ImageFont.load_default()
        font.size = 30

    im = Image.new("RGB", size, color=(0, 0, 0)) # 黑色背景
    draw = ImageDraw.Draw(im)
    for s, r in itertools.izip(list(val), region()):
        draw.text((r[0], r[1]), unicode(s), font=font, fill=(0, 255, 0))

    del draw
    # return im
    io = StringIO.StringIO()
    im.save(io, fmt)
    return io.getvalue()

if __name__ == '__main__':
#    check_code('abcd', font_file='/home/bamboo/townChiHuo/src/townChiHuo/static/fonts/wqy-zenhei.ttc').save('/home/bamboo/Pictures/test.png', 'PNG')
    check_code('abcde').save('/home/bamboo/Pictures/test.png', 'PNG')
        
    
    
    
    
