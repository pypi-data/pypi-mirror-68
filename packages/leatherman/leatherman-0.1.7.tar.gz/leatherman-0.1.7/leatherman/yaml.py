#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
output
"""
from ruamel import yaml


def str_presenter(dumper, data):
    str_tag = "tag:yaml.org,2002:str"
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar(str_tag, data, style="|")
    return dumper.represent_scalar(str_tag, data)


yaml.add_representer(str, str_presenter)


def list_presenter(dumper, data):
    list_tag = "tag:yaml.org,2002:seq"
    if len(data) > 1:
        if all([isinstance(item, str) for item in data]):
            return dumper.represent_sequence(list_tag, data, flow_style=False)
    return dumper.represent_sequence(list_tag, data)


yaml.add_representer(list, list_presenter)


def yaml_format(obj):
    class MyDumper(yaml.Dumper):
        MAX_SIMPLE_KEY_LENGTH = 256
        def represent_mapping(self, tag, mapping, flow_style=False):
            return yaml.Dumper.represent_mapping(self, tag, mapping, flow_style)

    return yaml.dump(obj, Dumper=MyDumper).strip()


def yaml_print(obj):
    return print(yaml_format(obj))
