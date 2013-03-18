#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

import web
from urls import urls

sys.path.append(os.path.dirname( \
        os.path.dirname(os.path.abspath(sys.argv[0]))))


if __name__ == '__main__':
    import townChiHuo.models
    print sys.prefix
    print urls
    print sys.path
    app = web.application(urls, globals())
    app.run()
