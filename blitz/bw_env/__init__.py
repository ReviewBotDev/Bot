# coding=utf8
"""
Пакет для работы с BW сервером.
"""
import os

def abs_path(rel):
    return os.path.realpath(os.path.join(os.path.dirname(__file__), rel))