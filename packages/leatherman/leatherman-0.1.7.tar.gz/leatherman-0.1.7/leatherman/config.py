#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config.py

"""

import os
import traceback
import configparser
from ruamel import yaml


class ConfigLoadError(Exception):
    def __init__(self, filename, errors):
        msg = f"config load error: filename={filename} errors={errors}"
        super(ConfigLoadError, self).__init__(msg)


def load_yaml_or_json(filename):
    with open(filename) as f:
        return yaml.safe_load(f)


def load_ini_or_cfg(filename):
    parser = configparser.ConfigParser()
    parser.read(filename)
    sections = {}
    for section in parser.sections():
        options = {}
        for option in parser.options(section):
            value = parser.get(section, option)
            options[option] = value
            sections[section] = options
    return sections


def load_config(*filenames, must_exist=False):
    cfg = {}
    errors = []
    for filename in [
        os.path.expanduser(filename) for filename in filenames if filename
    ]:
        if filename and os.path.isfile(filename):
            try:
                cfg.update(load_ini_or_cfg(filename))
            except Exception as ex1:
                errors += traceback.format_exc()
                try:
                    cfg.update(load_yaml_or_json(filename))
                except Exception as ex2:
                    errors += traceback.format_exc()
                    raise ConfigLoadError(filename, errors)
        elif must_exist:
            raise FileNotFoundError(filename)
    return cfg
