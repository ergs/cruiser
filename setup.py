#!/usr/bin/env python
# coding=utf-8
"""The cruiser installer."""
from __future__ import print_function
import os
import sys
try:
    from setuptools import setup
    from setuptools.command.develop import develop
    HAVE_SETUPTOOLS = True
except ImportError:
    from distutils.core import setup
    HAVE_SETUPTOOLS = False

from cruiser import __version__ as CRUISER_VERSION


def main():
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r') as f:
        readme = f.read()
    skw = dict(
        name='cruiser',
        description='A simple UI for Cyclus',
        long_description=readme,
        license='BSD',
        version=CRUISER_VERSION,
        author='Anthony Scopatz',
        maintainer='Anthony Scopatz',
        author_email='scopatz@gmail.com',
        url='https://github.com/ergs/cruiser',
        platforms='Cross Platform',
        classifiers=['Programming Language :: Python :: 3'],
        packages=['cruiser'],
        package_dir={'cruiser': 'cruiser'},
        #package_data={'cruiser': ['templates/*', 'static/*.*', 'static/img/*.*']},
        #scripts=['scripts/cruiser'],
        #zip_safe=False,
        )
    if HAVE_SETUPTOOLS:
        skw['setup_requires'] = []
        #skw['install_requires'] = ['Jinja2', 'pymongo']
    setup(**skw)


if __name__ == '__main__':
    main()
