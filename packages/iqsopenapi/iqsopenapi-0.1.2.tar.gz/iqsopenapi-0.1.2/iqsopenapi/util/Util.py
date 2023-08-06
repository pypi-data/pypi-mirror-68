# -*- coding: utf-8 -*-
import time
import sys
import os

def ExecutedTime(func):
    start = time.time()
    result = func()
    end = time.time()
    escape = end - start
    return escape, result

def Minimum(values, func):
    value = None
    last = None
    for x in values:
        result = func(x)
        if not last or last > result:
            value = x
            last = result
    return value