#!/usr/bin/env python
'''Add a way to default arguments from specified envvar or fallback'''

import os


def add_defaults(envvar, fallback=None):
    '''Set variable default from environment or fallback value'''
    if envvar in os.environ:
        return os.environ[envvar]
    return fallback
