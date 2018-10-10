#!/usr/bin/python3
# coding: utf-8

import hashlib, os, zipfile, sys, locale, tools

rarfile = None
try:
    import rarfile
except:
    pass

chardet = None
try:
    import chardet
except ImportError:
    pass

def is_rar(fn):
    with open(fn, "rb") as f:
        magic = f.read(4)
    return magic == b'Rar!'

def is_zip(fn):
    with open(fn, "rb") as f:
        magic = f.read(2)
    return magic == b'PK'

def is_archive(fn):
    return is_rar(fn) or is_zip(fn)

def is_image(fn):
    ext_fn = os.path.splitext(fn)[-1].lower()

    return ext_fn in \
            (".jpeg", ".jpg", ".png", ".gif", ".bmp", ".webp")

def every_files_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for name in files:
            yield os.path.join(root, name)

def load(path):
    return { hashlib.md5(fn.encode('utf-8')).hexdigest(): fn \
            for fn in filter(is_archive, every_files_in_directory(path)) }

class Archive(object):
    def __init__(self, path):
        self.path = path

        if rarfile and is_rar(self.path):
            with rarfile.RarFile(self.path, "r") as f:
                self.fnlist = [ e for e in f.namelist() if is_image(e) ]
                tools.alphanumeric_sort(self.fnlist)
            return

        if is_zip(self.path):
            with zipfile.ZipFile(self.path, "r") as f:
                self.fnlist = [ e for e in f.namelist() if is_image(e) ]
                tools.alphanumeric_sort(self.fnlist)
            return

        raise RuntimeError("Cannot open rar: please install python-rarfile")

    def read(self, pid):
        if rarfile and is_rar(self.path):
            with rarfile.RarFile(self.path, "r") as f:
                return f.read(self.fnlist[pid])

        with zipfile.ZipFile(self.path, "r") as f:
            return f.read(self.fnlist[pid])

        raise RuntimeError("Cannot open rar: please install python-rarfile")
