#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    "index", 
    "user", 
    ]

try:
    import index
    import user
    import permission
    
except ImportError as e:
    print e[0]
