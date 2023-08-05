# -*- coding: utf-8 -*-

def printWarning(msg):
    print("[WARNING] ", msg)

def printFatal(msg):
    print("[FATAL] ", msg)

def printException(msg):
    print("[EXCEPTION] ", msg)

def printInfo(msg):
    print("[INFO] ", msg)

def raiseException(msg):
    raise Exception(msg)

def read_dict(fn):
    return set([word.strip() for word in open(fn, encoding="utf8")])
