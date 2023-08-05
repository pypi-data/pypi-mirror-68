#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

from crwlr.statics import DASH, WHITESPACE, CROSSREF_DICTKEY_REFERENCETITLE


def check_re_match(regex, str_: str):
    p = re.compile(regex, re.IGNORECASE)
    match = p.match(str_)
    res = match.group() if match else False

    return res


def get_fact_key(lang, date_id, author_id, medium_id):
    return DASH.join([str(lang.lower()), str(date_id), author_id, medium_id])


def name_from(given_name, surname):
    return WHITESPACE.join([given_name, surname])


def reference_title(reference):
    for key in CROSSREF_DICTKEY_REFERENCETITLE:
        if key in reference:
            return reference[key]
    return False
