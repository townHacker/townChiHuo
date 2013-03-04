#!/usr/bin/env python
# -*- coding: utf-8 -*-

# start the web for test

import web
from urls import urls

if __name__ == '__main__':
    print urls
    app = web.application(urls, globals())
    app.run()
