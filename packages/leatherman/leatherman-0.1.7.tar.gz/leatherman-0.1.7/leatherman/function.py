#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect


def docstr(*args, **kwargs):
    frame = inspect.currentframe().f_back
    funcname = frame.f_code.co_name
    globals_ = frame.f_globals
    func = globals_[funcname]
    func.__doc__ = func.__doc__.format(*args, **kwargs)
    return func.__doc__
