#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def jsonify(string):
    return json.loads(str(string))


def json_print(obj, *exclusions):
    [obj.pop(exclusion, None) for exclusion in exclusions]
    print(json.dumps(obj, indent=2, sort_keys=True))
