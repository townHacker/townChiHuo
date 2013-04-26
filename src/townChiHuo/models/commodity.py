#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from townChiHuo.models.model import Model
from townChiHuo import db_schema
from townChiHuo.util import mongodb_hack as db_hack
from townChiHuo.models.error import GeneralError


class Commodity(Model):
    '''
    商品
    commodity_id: 商品id
    comm_name: 商品名称
    brief_name: 简短名称
    comm_desc: 商品描述
    comm_type: 商品类型
    comm_params: 商品参数
    comm_figure: 商品图像

    disabled # 禁用/启用
    disabled_date # 禁用时间
    disabled_desc # 禁用描述
    '''
    def __init__(self, doc=None):
        super(Commodity, self).__init__(doc=doc)


class CommodityType(Model):
    '''
    商品类型
    commodity_type_id: 商品类型id
    type_name: 类型名称
    type_desc: 类型描述
    type_parent_id: 父类型Id

    disabled # 禁用/启用
    disabled_date # 禁用时间
    disabled_desc # 禁用描述
    '''
    def __init__(self, doc=None):
        super(CommodityType, self).__init__(doc=doc)


def commodity_add(comm_name, comm_type_id, brief_name=None, comm_desc=None, \
                      *comm_figure, **comm_params):
    '''
    商品添加
    '''
    try:
        comm_c = db_hack.connect(collection=db_schema.COMMODITY)
        comm_name = unicode(comm_name)
        if not comm_type:
            raise GeneralError(u"商品类型错误")
        elif not comm_name \
                and None is not comm_c.find_one({"name": comm_name}):
            raise GeneralError(u"已存在相同的商品名称")
        else:
            comm_m = Commodity()
            comm_m.commodity_id = unicode(uuid.uuid4())
            comm_m.comm_type_id = comm_type_id
            comm_m.comm_name = comm_name
            comm_m.brief_name = brief_name \
                if brief_name else comm_type
            comm_m.comm_desc = comm_desc
            comm_m.comm_figure = comm_figure
            comm_m.comm_params = comm_params

            object_id = comm_c.insert(comm_m.get_doc())
            return Commodity(doc=comm_c.find_one({"_id": object_id}))
    finally:
        del comm_c


def commodity_type_add(type_name, type_desc=None, type_parent=None):
    '''
    商品类型添加
    '''
    comm_type_c = db_hack.connect(collection=db_schema.COMMODITY_TYPE)
    try:
        type_name = unicode(type_name)
        if not type_name \
                and  None is not comm_type_c.find_one({'name': type_name}):
            raise GeneralError(u"已存在相同的商品类型名称")
        else: # 商品类型名称不存在, 添加
            comm_type_m = CommodityType()
            comm_type_m.commodity_type_id = unicode(uuid.uuid4())
            comm_type_m.type_name = type_name
            comm_type_m.type_desc = type_desc
            comm_type_m.type_parent_id = \
                type_parent.commodity_type_id if type_parent else None
            
            objectId = comm_type_c.insert(comm_type_m.get_doc())
            return CommodityType(doc=comm_type_c.find_one({"_id": objectId}))
    finally:
        del comm_type_c
        

def get_commodity_type(*type_parent_id, **type_id):
    '''
    获取商品类型, 或通过指定的商品类型, 获取所有的子类型
    '''
    comm_type_c = db_hack.connect(collection=db_schema.COMMODITY_TYPE)
    try:
        if type_id:
            return comm_type_c.find(type_id)
        elif type_parent_id:
            return comm_type_c.find({
                    "type_parent_id": { "$in": type_parent_id }, 
                    })
        else:
            return comm_type_c.find()
    finally:
        del comm_type_c


        
        

