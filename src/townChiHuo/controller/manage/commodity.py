#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
import itertools

from townChiHuo.util.mako_render import mako_render
from townChiHuo.models.error import GeneralError
from townChiHuo.models import commodity

class Commodity(object):

    def GET(self, *path):

        comm_iter = commodity.get_commodity()

        comm_type_root_iter = commodity.get_commodity_type(None)
        
        comm_type_item = \
            dict([(t_item['commodity_type_id'], t_item['type_name']) \
                              for t_item in commodity.get_commodity_type()])
        
        
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/commodity.tmpl',
                           commodity = comm_iter, 
                           commodity_type_root = comm_type_root_iter,
                           comm_type_name = comm_type_item)


class CommodityAdd(object):
    def POST(self, *path):
        try: 
            form = web.input(
                'commodity_name',
                commodity_desc=None,
                commodity_type_id=None)
            if not form.commodity_name:
                raise GeneralError(u'请添写商品名称')
            elif not form.commodity_type_id:
                raise GeneralError(u'请选择商品类型')
            
            commodity_new = commodity.commodity_add(form.commodity_name,
                                    form.commodity_type_id,
                                    comm_desc=form.commodity_desc)
            result = dict( isSucceed = True,
                           msg = u"添加商品成功")
        except GeneralError as err:
            result = dict( isSucceed = False,
                           msg = err.value )
            
        web.header('Content-Type', 'application/json')
        return json.dumps(result)


class CommodityType(object):
    def GET(self, *path):
        comm_type_iter = commodity.get_commodity_type()
        comm_type_iter, comm_type_iter1 = itertools.tee(comm_type_iter)
        comm_type_name = \
            dict([(item['commodity_type_id'], item['type_name']) \
                            for item in comm_type_iter1])
        comm_type_root_iter = commodity.get_commodity_type(None)
        
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/commodity_type.tmpl',
                           commodity_type =comm_type_iter,
                           commodity_type_root =comm_type_root_iter,
                           commodity_type_name = comm_type_name, 
                           )

    def POST(self, *path):
        p_in = web.input('type_parent_id')
        comm_type_iter = commodity.get_commodity_type(p_in.type_parent_id)
        comm_types = [{'id': item['commodity_type_id'],
                       'name': item['type_name'] } for item in comm_type_iter]
        
        web.header('Content-Type', 'application/json')
        return json.dumps({ 'types': comm_types })
        

class CommodityTypeAdd(object):
    def POST(self, *path):
        form_in = web.input("type_name", "type_parent_id", type_desc=None)
        try:
            if form_in.type_parent_id:
                type_parent = \
                    commodity.CommodityType(
                    doc=commodity.get_commodity_type(
                        commodity_type_id=form_in.type_parent_id)[0])
            else:
                type_parent = None

            comm_type_m = \
                commodity.commodity_type_add(form_in.type_name,
                                             type_desc=form_in.type_desc, 
                                             type_parent=type_parent)
            result = dict(
                isSucceed = True,
                msg = "添加商品类型成功" )
        except GeneralError as err:
            result = dict( isSucceed = False, msg = err.value )

        web.header('Content-Type', 'application/json')
        return json.dumps(result)
