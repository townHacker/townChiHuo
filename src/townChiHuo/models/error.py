#!/usr/bin/env python
# -*- coding: utf-8 -*-

__metaclass__ = type

class GeneralError(Exception):
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)

    def __unicode__(self):
        return unicode(self.value)
