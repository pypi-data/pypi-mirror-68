#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import ast
import inspect
from pprint import pformat

from .isinstance import *

__all__ = ["dbg"]


class FmtKeyError(Exception):
    def __init__(self, keys):
        msg = 'fmt error; key not found in keys: ' + ' '.join(keys)
        super(FmtKeyError, self).__init__(msg)

def dbg(*args, **kwargs):
    logger = kwargs.pop("logger", None)
    frame = inspect.currentframe().f_back
    return _dbg(args, kwargs, frame, logger=logger)


def _create_format(name):
    try:
        return str(ast.literal_eval(name))
    except Exception:
        return name + "({" + name + '_type})="{' + name + '}"'


_dbg_regex = re.compile(r"p?dbg\s*\((.+?)\)$")


def _dbg(args, kwargs, frame, logger=None):
    caller = inspect.getframeinfo(frame)
    string = f"DBG:{os.path.relpath(caller.filename)}:{caller.lineno} "
    instance = frame.f_locals.get("self", None)
    if instance:
        string += instance.__class__.__name__ + "."
    string += frame.f_code.co_name + "(): "
    if args or kwargs:
        context = inspect.getframeinfo(frame).code_context
        callsite = "".join([line.strip() for line in context])
        match = _dbg_regex.search(callsite)
        if match:
            params = [
                param.strip() for param in match.group(1).split(",") if "=" not in param
            ]
        names = params[: len(args)] + list(kwargs.keys())
        string += " ".join([_create_format(name) for name in names])
        arg_types = {name + "_type": type(arg) for name, arg in zip(names, args)}
        kwarg_types = {key + "_type": type(value) for key, value in kwargs.items()}
        kwargs.update(arg_types)
        kwargs.update(kwarg_types)
    else:
        string += "locals:\n{locals}"
    result = _fmt(string, args, kwargs, frame, do_print=logger is None)
    if logger:
        logger.debug(result)
    return result


def _fmt_dict(obj):
    if isdict(obj) or islist(obj):
        return pformat(obj)
    return str(obj)


def _fmt(string, args, kwargs, frame, do_print=False):
    try:
        gl = {"locals": frame.f_locals, "globals": frame.f_globals}
        gl.update(frame.f_globals)
        gl.update(frame.f_locals)
        gl.update(kwargs)
        if frame.f_code.co_name == "<listcomp>":
            gl.update(frame.f_back.f_locals)
        result = string.format(*args, **{k: _fmt_dict(v) for k, v in gl.items()})
    except KeyError as ke:
        raise FmtKeyError(gl)
    if do_print:
        print(result)
    return result
