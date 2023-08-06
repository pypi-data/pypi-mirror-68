#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
human friendly functions
"""

import re
import datetime

WEEKS = "(?P<weeks>[0-9]+w)?"
DAYS = "(?P<days>[0-9]+d)?"
HOURS = "(?P<hours>[0-9]+h)?"
MINUTES = "(?P<minutes>[0-9]+m)?"
SECONDS = "(?P<seconds>[0-9]+s)?"
PARSE = re.compile(WEEKS + DAYS + HOURS + MINUTES + SECONDS)
VALIDATE = re.compile("^([0-9]+(w|d|h|m|s))+$")


class FriendlyTimedeltaParseError(Exception):
    def __init__(self, string):
        msg = "friendly.timedelta parse error for string: " + string
        super(FriendlyTimedeltaParseError, self).__init__(msg)


def timedelta(string):
    if VALIDATE.match(string):
        match = PARSE.match(string)
        if not match:
            raise FriendlyTimedeltaParseError(string)
        kwargs = {k: int(v[:-1]) for k, v in match.groupdict().items() if v is not None}
        return datetime.timedelta(**kwargs)
    raise FriendlyTimedeltaParseError(string)
