#!/usr/bin/env python
# -*- coding: utf-8 -*-

import web
import json
import itertools

from bson.objectid import ObjectId

from townChiHuo.util.mako_render import mako_render
from townChiHuo.models.error import GeneralError
from townChiHuo.models import commodity

class Commodity(object):

    def GET(self, *path):

        comm_iter = commodity.Commodity.objects()

        comm_type_root_iter = \
            commodity.CommodityType.objects(type_parent=None)

        iters = itertools.tee(comm_iter, 2)
        
        comm_type_item = \
            dict([(unicode(t_item['id']), t_item['comm_type']['type_name']) \
                              for t_item in iters[0]])
                
        web.header('Content-Type', 'text/html')
        return mako_render('/manage/commodity.tmpl',
                           commodity = iters[1], 
                           commodity_type_root = comm_type_root_iter,
                           comm_type_name = comm_type_item)


class CommodityAdd(object):
    def POST(self, *path):
        try: 
            form = web.input('commodity_name', commodity_desc=None,
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
            dict([(item['id'], item['type_name']) \
                            for item in comm_type_iter1])
        comm_type_root_iter = commodity.get_commodity_type(None)

        web.header('Content-Type', 'text/html')
        return mako_render('/manage/commodity_type.tmpl',
                           commodity_type =comm_type_iter,
                           commodity_type_root =comm_type_root_iter,
                           commodity_type_name = comm_type_name
                           )

    def POST(self, *path):
        p_in = web.input('type_parent_id')
        parent_type = commodity.CommodityType.objects(
            id=ObjectId(p_in.type_parent_id)).first()
        comm_type_iter = parent_type.get_child_commType()
        comm_types = [{'id': item['id'],
                       'name': item['type_name'] } for item in comm_type_iter]
        
        web.header('Content-Type', 'application/json')
        return json.dumps({ 'types': comm_types })
        

class CommodityTypeAdd(object):
    def POST(self, *path):
        form_in = web.input("type_name", "type_parent_id", type_desc=None)
        try:
            if not form_in.type_name:
                raise GeneralError("请填写类型名称")
                
            if form_in.type_parent_id:
                type_parent = \
                    commodity.CommodityType.objects(
                        id=ObjectId(form_in.type_parent_id)).first()
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


class CommodityParam(object):
    def GET(self, *path):
        pass
        
class CommodityParamAdd(object):
    def POST(self, *path):
        form_in = web.input("type_id", "params")
        
