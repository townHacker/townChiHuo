#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid

from bson.objectid import ObjectId
from mongoengine import *
from mongoengine.context_managers import no_dereference

from townChiHuo.models.model import Model
from townChiHuo import db_schema
from townChiHuo.util import mongodb_hack as db_hack
from townChiHuo.models.error import GeneralError


class CommodityParam(EmbeddedDocument):
    '''
    商品参数
    param_name: 参数名称
    param_value: 参数值
    param_type: 参数类型
        - str 字符类型
        - num 数值类型
    optional_value: 可选值 （用于单选或多选） a list []
    is_multiple: 是否多选    True or False, 当且仅当 optional_value 不为空时
    '''
    param_name = StringField(max_length=200, required=True, unique=True)
    param_value = DynamicField()
    param_type = StringField(choices=['str', 'num'])
    optional_value = ListField(DynamicField())
    is_multiple = BooleanField()
    

    
class CommodityType(Document):
    '''
    商品类型
    commodity_type_id: 商品类型id
    type_name: 类型名称
    type_desc: 类型描述
    type_parent_id: 父类型Id

    disabled # 禁用/启用
    disabled_date # 禁用时间
    disabled_desc # 禁用描述

    type_params # 类型参数
    '''
    type_name = StringField(max_length=200, required=True)
    type_desc = StringField(max_length=1000, required=True)
    type_parent = ReferenceField('self')
    disabled = BooleanField()
    disabled_date = DateTimeField()
    disabled_desc = StringField()

    type_params = ListField(EmbeddedDocumentField(CommodityParam))

    meta = {
        'collection' : db_schema.COMMODITY_TYPE,
        'allow_inheritance': True
    }

    
    def get_child_commType(self, include_disabled=False):
        '''
        得到所有商品子类型
        include_disabled = True 将包含已被禁用的子类型, 默认为 False
        '''
        with no_dereference(self.__class__) as CommodityType:
            return CommodityType.objects(__raw__={
                'type_parent' : self.id
            })
        

    def add_commodityParam(self, *comm_params):
        '''
        添加商品参数
        '''
        if self.type_params:
            comm_params[len(comm_params):] = self.type_params
            
        self.type_params = comm_params
        self.save()
        self.reload()

        


class Commodity(Document):
    '''
    商品
    commodity_id: 商品id
    comm_name: 商品名称
    brief_name: 简短名称
    comm_desc: 商品描述
    comm_type_id: 商品类型
    comm_params: 商品参数
    comm_figure: 商品图像

    disabled # 禁用/启用
    disabled_date # 禁用时间
    disabled_desc # 禁用描述
    '''
    comm_name = StringField(max_length=200, required=True)
    brief_name = StringField(max_length=100)
    comm_desc = StringField()
    comm_type = ReferenceField(CommodityType)
    comm_params = ListField(EmbeddedDocumentField(CommodityParam))
    comm_figure = ListField(StringField())
    disabled = BooleanField()
    disabled_date = DateTimeField()
    disabled_desc = StringField()

    meta = {
        'collection': db_schema.COMMODITY,
        'allow_inheritance': True
    }
    



def get_commodity(*commodity_id):
    if commodity_id:
        return Commodity.objects(
            __raw__={'id': {'$in': commodity_id}})
    else:
        return Commodity.objects()



def commodity_add(comm_name, comm_type_id,
                  brief_name=None, comm_desc=None,
                  comm_figure=[], comm_params=[]):
    '''
    商品添加
    '''
    comm_name = unicode(comm_name)
    if not comm_type_id:
        raise GeneralError(u"商品类型错误")
    elif not comm_name \
         and None is not \
         Commodity.objects(__raw__={"name": comm_name}).first():
        raise GeneralError(u"已存在相同的商品名称")
    else:
        comm_m = Commodity()
        comm_m.comm_type = \
            CommodityType.objects(id=ObjectId(comm_type_id)).first()
        comm_m.comm_name = comm_name
        comm_m.brief_name = brief_name \
            if brief_name else comm_name
        comm_m.comm_desc = comm_desc
        comm_m.comm_figure = comm_figure
        comm_m.comm_params = comm_params

        comm_m.save()
        return comm_m



def commodity_type_add(type_name, type_desc=None, type_parent=None):
    '''
    商品类型添加
    '''
    type_name = unicode(type_name)
    if not type_name \
       and None is not \
       CommodityType.objects(__raw__={'name': type_name}).first():
        raise GeneralError(u"已存在相同的商品类型名称")
    else: # 商品类型名称不存在, 添加
        comm_type_m = CommodityType()
        comm_type_m.type_name = type_name
        comm_type_m.type_desc = type_desc
        comm_type_m.type_parent = type_parent
        
        comm_type_m.save()
        return comm_type_m
         

def get_commodity_type(*type_parent_id):
    '''
    获取商品类型, 或通过指定的商品类型, 获取所有的子类型
    '''
    if type_parent_id:
        return CommodityType.objects(__raw__={
            "type_parent": { "$in": type_parent_id }, 
        })
    else:
        return CommodityType.objects()


def commodity_param_add(comm_type_id, type_param):
    '''
    向商品类型中添加商品参数
    '''
    pass
    


