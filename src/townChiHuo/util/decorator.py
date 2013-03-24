#!/usr/bin/env python
# -*- coding: utf-8 -*-



from townChiHuo.settings import action_auth

def action_auth_decorator(action_id, \
                              action_name, \
                              action_code, \
                              default_permission):
    def wrap(func):

        if action_id not in action_auth:
            action_auth[action_id] = dict(
                action_id = action_id,
                action_name = action_name,
                action_code = action_code,
                default_permission = default_permission
                )
        
        def wrapped_func(*args):
            return func(*args)

        wrapped_func.__dict__.update(func.__dict__)
        wrapped_func.__name__ = func.__name__
        wrapped_func.__doc__ = func.__doc__

        # 获取 action_id
        wrapped_func.__dict__['get_action_id'] = \
            lambda : action_id

        # 获取 action_name
        wrapped_func.__dict__['get_action_name'] = \
            lambda : action_auth[action_id]['action_name']
        
        # 获取 action_code
        wrapped_func.__dict__['get_action_code'] = \
            lambda: action_auth[action_id]['action_code']

        # 获取 default_permission
        wrapped_func.__dict__['get_default_permission'] = \
            lambda: action_auth[action_id]['default_permission']
        
        return wrapped_func
    return wrap

