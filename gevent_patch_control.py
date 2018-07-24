# coding:utf-8

import sys
from threading import local
from gevent import monkey

__all__ = ['patch', 'thread_use_gevent', 'thread_use_original',
           'default_use', 'GEVENT', 'ORIGINAL']

GEVENT = 0
ORIGINAL = 1
_tls = local()
_default_use = ORIGINAL


def default_use(use=None):
    if use == None:
        return _default_use
    _default_use = use


default_use.__doc__ = '''default_use(use=None)

set/get default behavor on the thread never call thread_use_gevent / thread_use_original

valid use values:
  (set) gevent_patch_control.GEVENT
  (set) gevent_patch_control.ORIGINAL
  (get) None
'''


def thread_use_gevent():
    _tls.use = GEVENT


thread_use_gevent.__doc__ = '''thread_use_gevent()

enable gevent patch on current thread
'''


def thread_use_original():
    _tls.use = ORIGINAL


thread_use_gevent.__doc__ = '''thread_use_original()

disable gevent patch on current thread
'''


class _mock_caller():
    def __init__(self, gevent_obj, original_obj):
        self.gevent_obj = gevent_obj
        self.original_obj = original_obj

    def __call__(self, *args, **kwargs):
        if hasattr(_tls, 'use'):
            use_gevent = _tls.use == GEVENT
        else:
            use_gevent = _default_use == GEVENT

        if use_gevent:
            return self.gevent_obj(*args, **kwargs)
        return self.original_obj(*args, **kwargs)

def _patch_no_check(module):
    for attrname in module.__all__:
        obj = getattr(module, attrname)
        if hasattr(obj, '__module__') and obj.__module__.startswith('gevent.'):
            original_obj = monkey.get_original(module.__name__, attrname)
            setattr(module, attrname, _mock_caller(obj, original_obj))

def patch(modules):
    if not isinstance(modules, list):
        modules = [modules]

    for module in modules:
        if isinstance(module, str):
            module = sys.modules[module]
        _patch_no_check(module)


patch.__doc__ = '''patch(module(s))

patch module to control gevent patch

module:
  (list of) module object / name (s) to patch, should be already patched by gevent

examples:
gevent_patch_control.patch('socket')

import os
gevent_patch_control.patch(os)

import os
gevent_patch_control.patch([os, 'socket'])
'''

#todo: add selective args
def patch_all():
    for module in sys.modules:
        if monkey.is_module_patched(module.__name__):
            _patch_no_check(module)

patch.__doc__ = '''patch_all()

patch all modules already patched by gevent
'''