#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# File: ${FILE_NAME}
# Author: Raeid Saqur
# Email: rsaqur@cs.princeton.edu
# Created on: 13/04/2018
#
# This file is part of RSMLKit
# Distributed under terms of the MIT License

import os, sys
import importlib

__all__ = [
    'load_module', 'load_module_filename',
    'tuple_to_classname', 'classname_to_tuple',
    'load_class', 'module_vars_as_dict'
]

def load_module_filename(fn):
    assert fn.endswith('.py')
    realpath = os.path.realpath(fn)
    pos = realpath.rfind('/')
    dirname, module_name = realpath[0:pos], realpath[pos+1:-3]
    sys.path.insert(0, dirname)
    module = load_module(module_name)
    del sys.path[0]
    return module

def load_module(name):
    module = importlib.import_module(name)
    return module


def load_class(classname, exit_on_error=True):
    if isinstance(classname, str):
        classname = classname_to_tuple(classname)
    elif isinstance(classname, tuple):
        assert len(classname) == 2, 'Classname should be tuple of length 2 or a single string.'
    module_name, clz_name = classname
    try:
        module = load_module(module_name)
        clz = getattr(module, clz_name)
        return clz
    except ImportError as e:
        print('Cannot import {}.{}, with original error message: {}.'.format(module_name, clz_name, str(e)))
        if exit_on_error:
            exit(1)
    return None

def classname_to_tuple(classname):
    pos = classname.rfind('.')
    if pos == -1:
        return '', classname
    else:
        return classname[0:pos], classname[pos + 1:]

def tuple_to_classname(t):
    assert len(t) == 2, ('Only tuple with length 2 (module name, class name) can be converted to classname, '
            'got {}, {}.'.format(t, len(t)))

    return '.'.join(t)

def module_vars_as_dict(module):
    res = {}
    for k in dir(module):
        if not k.startswith('__'):
            res[k] = getattr(module, k)
    return res
