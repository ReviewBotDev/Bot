import datetime
import random
import sys

__all__ = [
    'cached_value',
    'get_methods_for',
    'make_https_host',
    'static_vars',
    'now_plus_delta',
]

class cached_value(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


def get_methods_for(clazz):
    return [method_name for method_name in dir(clazz) if callable(getattr(clazz, method_name))]


def make_https_host(host):
    if host is None or host.startswith('https://'):
        return host

    return 'https://' + host


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


def now_plus_delta(**kwargs):
    dt = datetime.datetime.now()
    return dt + datetime.timedelta(**kwargs)


def get_unique_name(base):
    return base.format(random.randint(0, sys.maxint))