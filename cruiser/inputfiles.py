"""Input file tools"""
import os
import sys
import pdb
import inspect
import traceback


class InputFile(object):
    """Base class for handling input files."""

    def __init__(self):
        self._sim = self.default()
        self._params = None

    def __call__(self):
        return self._sim

    @property
    def params(self):
        if self._params is None:
            self._params = tuple([k for k, v in inspect.getmembers(self)
                                  if isinstance(v, InParam)])
        return self._params

    def default(self):
        return {}


class InParam(object):
    """Descriptor class for inpute parameters"""

    def __init__(self, name, setter, default=None, widget=None):
        self.name = name
        self.private_name = '_' + name
        self.setter = setter
        self.default = default
        self.widget = widget

    def __get__(self, instance, owner):
        if instance is None:
            return self
        elif hasattr(instance, self.private_name):
            return getattr(instance, self.private_name)
        else:
            setattr(instance, self.private_name, self.default)
            return self.default

    def __set__(self, instance, value):
        setattr(instance, self.private_name, value)
        self.setter(value)


def inparam(default=None, widget=None):
    """Decorator for turning a method into an InParam"""
    def dec(f):
        return InParam(f.__name__, f, default=default, widget=widget)
    return dec
