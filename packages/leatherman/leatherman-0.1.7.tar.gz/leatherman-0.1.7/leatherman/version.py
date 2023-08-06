#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .git import describe
from .shell import cd


def get_version(path="."):
    try:
        try:
            with cd(path):
                value = open("VERSION").read().strip()
        except:  # noqa: E722
            value = describe()
    except:  # noqa: E722
        value = "UNKNOWN"
    version, *suffix = value.split("-")
    return version.replace("v", "") + (".dev{0}+{1}".format(*suffix) if suffix else "")


class Version(str):
    __instance = None

    def __new__(cls):
        if Version.__instance is None:
            value = get_version()
            Version.__instance = super(Version, cls).__new__(cls, value)
        return Version.__instance


version = Version()
