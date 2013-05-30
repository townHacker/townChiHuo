#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import StringIO
import itertools
import Image, ImageDraw, ImageFont


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

def figure_cut(img, zoom, top, left, width, height,
               n_width, n_height, save_file_name):
    '''
    图像裁剪：
      img: 图像文件的路径
      zoom: 缩放大小
      top: 左上角y坐标
      left: 左上角x坐标
      width: 裁剪区域的宽
      height: 裁剪区域的高
      n_width: 最终图片需要的宽度
      n_height: 最终图片需要的高度
      save_file_name: 最终图片的名称
    '''
    try:
        crop_region = (left, top, left + width + 1, top + height + 1)
        im = Image.open(img)
        n_size = (int(im.size[0] * zoom), int(im.size[1] * zoom))
        region =  im.resize(n_size).crop(crop_region)
        mask = Image.new('L', (n_width, n_height), color=0)
        box = ((n_width - width) /2, (n_height - height) /2,
               (n_width - width) / 2 + width, (n_height - height) / 2 + height)
        draw = ImageDraw.Draw(mask)
        draw.rectangle(box, fill=255)
        new_im = Image.new(im.mode, (n_width, n_height))
        new_im.paste(region, (box[0], box[1]))
        new_im.putalpha(mask)
        new_im.save(save_file_name, 'PNG')

        return True
    except IOError as e:
        print sys.exc_info()[0], e.args 
        return False
    

if __name__ == '__main__':
    # check_code('abcd', font_file='/home/bamboo/townChiHuo/src/townChiHuo/static/fonts/wqy-zenhei.ttc').save('/home/bamboo/Pictures/test.png', 'PNG')
    # check_code('abcde').save('/home/bamboo/Pictures/test.png', 'PNG')
    figure_cut('/home/bamboo/Project/test.jpg', .5, 10, 10, 150, 150, 200, 200,
               '/home/bamboo/Project/test_reault.png')
        
    
