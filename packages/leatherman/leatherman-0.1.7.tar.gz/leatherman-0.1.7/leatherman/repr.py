#!/usr/bin/env python3

def gen_repr(obj, **kwargs):
    fields = ', '.join([
        f'{key}={value}' for key, value in dict(obj.__dict__, **kwargs).items()
    ])
    return f'{obj.__class__.__name__}({fields})'

def __repr__(self):
    return gen_repr(self)
