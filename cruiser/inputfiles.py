"""Input file tools"""
import os
import sys
import pdb
import inspect
import importlib
import traceback


SCENARIO_DIR = os.path.join(os.path.dirname(__file__), 'scenarios')
SCENARIOS = tuple([os.path.splitext(f)[0] for f in os.listdir(SCENARIO_DIR)
                   if not f.startswith('_')])


class InputFile(object):
    """Base class for handling input files."""

    scenario = 'nemo'

    def __init__(self):
        self.sim = self.default()
        self.params = tuple([k for k, v in inspect.getmembers(self.__class__)
                             if isinstance(v, InParam)])

    def __call__(self):
        return self._sim

    def default(self):
        return {}


class InParam(object):
    """Descriptor class for input parameters"""

    def __init__(self, name, setter, default=None, widget=None, widget_kwargs=None):
        self.name = name
        self.private_name = '_' + name
        self.setter = setter
        self.default = default
        self.widget = widget
        self.widget_kwargs = {} if widget_kwargs is None else widget_kwargs
        self.widget_kwargs.pop('value', None)
        self.widget_kwargs.pop('description', None)

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
        self.setter(instance, value)


def inparam(default=None, widget=None, **widget_kwargs):
    """Decorator for turning a method into an InParam"""
    def dec(f):
        return InParam(f.__name__, f, default=default, widget=widget,
                       widget_kwargs=widget_kwargs)
    return dec


def load(name):
    """Loads a simulation from its module name."""
    mod = importlib.import_module('cruiser.scenarios.' + name)
    sim = mod.Simulation()
    return sim
