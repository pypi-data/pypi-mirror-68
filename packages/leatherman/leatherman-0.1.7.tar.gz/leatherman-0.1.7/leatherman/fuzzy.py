#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from enum import Enum
from fnmatch import fnmatch
from collections import OrderedDict


class MatchType(Enum):
    EXACT = 0
    IGNORECASE = 1
    PREFIX = 2
    SUFFIX = 3
    CONTAINS = 4
    GLOB = 5
    REGEX = 6


class InvalidFuzzyTypeError(Exception):
    def __init__(self, obj):
        message = f"type(obj)={type(obj)} is not dict or list"
        super(InvalidFuzzyTypeError, self).__init__(message)


MATCH_FUNCS = {
    MatchType.EXACT: lambda item, pattern: pattern == item,
    MatchType.IGNORECASE: lambda item, pattern: pattern.lower() == item.lower(),
    MatchType.PREFIX: lambda item, pattern: fnmatch(item, pattern + "*"),
    MatchType.SUFFIX: lambda item, pattern: fnmatch(item, "*" + pattern),
    MatchType.CONTAINS: lambda item, pattern: pattern in item,
    MatchType.GLOB: lambda item, pattern: fnmatch(item, pattern),
    MatchType.REGEX: lambda item, pattern: re.search(item, pattern),
}

DEFAULT_MATCH_TYPES = [
    MatchType.EXACT,
    MatchType.IGNORECASE,
    MatchType.PREFIX,
    MatchType.CONTAINS,
]


def match_item(item, patterns, match_type, include):
    match_func = MATCH_FUNCS[match_type]
    if include:
        return any([match_func(item, pattern) for pattern in patterns])
    return all([not match_func(item, pattern) for pattern in patterns])


def match_items(items, patterns, match_types, include=True):
    for match_type in match_types:
        results = [
            item for item in items if match_item(item, patterns, match_type, include)
        ]
        if results:
            return results
    return []

class FuzzyTuple(tuple):
    def __new__(cls, *args, **kwargs):
        self._type = type(args[0])
        return super().__new__(cls, tuple(*args))

    def __init__(self, *args, **kwargs):
        self._match_types = kwargs.pop("match_types", DEFAULT_MATCH_TYPES)

    def include(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            include=True,
        )
        return FuzzyTuple(items)

    def exclude(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            include=False,
        )
        return FuzzyTuple(items)

    def defuzz(self):
        return tuple(item for item in self.__iter__())

    def __repr__(self):
        return repr(tuple(self))


class FuzzyList(list):
    def __init__(self, *args, **kwargs):
        self._type = type(args[0])
        self._match_types = kwargs.pop("match_types", DEFAULT_MATCH_TYPES)
        super().__init__(*args, **kwargs)

    def include(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            include=True,
        )
        return FuzzyList(items)

    def exclude(self, *patterns, match_types=None):
        items = match_items(
            [item for item in self.__iter__()],
            patterns,
            match_types or self._match_types,
            include=False,
        )
        return FuzzyList(items)

    def defuzz(self):
        return [item for item in self.__iter__()]


class FuzzyDict(OrderedDict):
    def __init__(self, *args, **kwargs):
        self._type = type(args[0])
        self._match_types = kwargs.pop("match_types", DEFAULT_MATCH_TYPES)
        super().__init__(*args, **kwargs)

    def include(self, *patterns, match_types=None):
        items = match_items(
            self.keys(), patterns, match_types or self._match_types, include=True
        )
        return FuzzyDict({item: self.get(item) for item in items})

    def exclude(self, *patterns, match_types=None):
        items = match_items(
            self.keys(), patterns, match_types or self._match_types, include=False
        )
        return FuzzyDict({item: self.get(item) for item in items})

    def defuzz(self):
        if self._type.__name__ == 'dict':
            return dict(self.items())
        elif self._type.__name__ == 'collections.OrderedDict':
            return OrderedDict(self.items())
        raise Exception(f"unknown type: {self._type}")


def fuzzy(obj):
    if isinstance(obj, tuple):
        return FuzzyTuple(obj)
    elif isinstance(obj, list):
        return FuzzyList(obj)
    elif isinstance(obj, dict):
        return FuzzyDict(obj)
    raise InvalidFuzzyTypeError(obj)


if __name__ == "__main__":
    f = fuzzy(["a", "b"])
    print(f"f={f.items}")
