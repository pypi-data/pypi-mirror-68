"""
git utilities
"""

from .shell import call, cd


def reporoot(path="."):
    with cd(path):
        return call("git rev-parse --show-toplevel")[1].strip()


def describe(path="."):
    with cd(path):
        return call("git describe --abbrev=7")[1].strip()


def subs2shas(path="."):
    lines = call("cd %s && git submodule" % path)[1].strip().split("\n")
    return dict([(item[1], item[0]) for item in [line.split() for line in lines]])
