#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import web
from web.session import Store

__all__ = [
    'MemcachedStore', 
    ]

class MemcachedStore(Store):
    '''
    session be stored in memcached
    inherit web.session.Store(see web.py web framework session.py source file)
    '''
    def __init__(self, mc):
        self._mc = mc;
    
    def __contains__(self, key):
        return True if self._mc.get(key) else False

    def __getitem__(self, key):
        value = self._mc.get(key)
        if value:
            value['atime'] = time.time()
            self._mc.set(key, value)
        return value

    def __setitem__(self, key, value):
        now = time.time()
        value['atime'] = now
        self._mc.set(key, value, web.config.session_parameters['timeout'])
        
    def __delitem__(self, key):
        self._mc.delete(key)
    

    def cleanup(self, timeout):
        pass

    def encode(self, session_dict):
        '''
        encodes session dict as a string
        '''
        super(MemcachedStore, self).encode(session_dict)

    def decode(self, session_data):
        '''
        decodes the data to get back the session dict
        '''
        super(MemcachedStore, self).decode(session_data)


if __name__ == '__main__':
    print web.config.session_parameters
