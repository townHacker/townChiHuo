#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    "index",
    "static_file",
    
    "manage", 
    ]

try:
    import index
    import static_file

    import manage
    
except ImportError as e:
    print e[0]
