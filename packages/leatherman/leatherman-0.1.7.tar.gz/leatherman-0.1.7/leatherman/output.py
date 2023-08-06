#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from .json import json_print
from .yaml import yaml_print

OUTPUT = ["json", "yaml"]


def output_print(json, output):
    if output == "yaml":
        yaml_print(json)
    elif output == "json":
        json_print(json)


def default_output():
    return OUTPUT[int(sys.stdout.isatty())]
