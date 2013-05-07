#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import web
from web.session import Store

try:
    import pylibmc as memcache
except:
    import memcache

__all__ = [
    'MemcachedStore', 
    ]

class MemcachedStore(Store):
    '''
    session be stored in memcached
    inherit web.session.Store(see web.py web framework session.py source file)
    '''
    
    def __init__(self, mc):
        if hasattr(memcache, 'ClientPool'):
            self.pool = memcache.ClientPool(mc, 4)
        else:
            self._mc = mc;

    def _get(self, key):
        if hasattr(self, 'pool'):
            with self.pool.reserve() as mc:
                return mc.get(key)
        else:
            return self._mc.get(key)

    def _set(self, *args):
        if hasattr(self, 'pool'):
            with self.pool.reserve() as mc:
                mc.set(*args)
        else:
            self._mc.set(*args)

    def _delete(self, key):
        if hasattr(self, 'pool'):
            with self.pool.reserve() as mc:
                mc.delete(key)
        else:
            self._mc.delete(key)
    
    
    def __contains__(self, key):
        return True if self._get(key) else False

    def __getitem__(self, key):
        print 'get_session(memcache_key): ', key
        value = self._get(key)
        if value:
            value['atime'] = time.time()
            self._set(key, value)
        return value

    def __setitem__(self, key, value):
        print 'set_session(memcache_key): ', key
        now = time.time()
        value['atime'] = now
        self._set(key, value, web.config.session_parameters['timeout'])
        
    def __delitem__(self, key):
        print 'del_session(memcache_key): ', key
        self._delete(key)
    

    def cleanup(self, timeout):
        pass

    def encode(self, session_dict):
        '''
        encodes session dict as a string
        '''

    def decode(self, session_data):
        '''
        decodes the data to get back the session dict
        '''


if __name__ == '__main__':
    print web.config.session_parameters
