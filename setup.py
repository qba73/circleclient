#!/usr/bin/env python
"""
Setup script for circleclient.

"""

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.rst')) as f:
    LONG_DESCRIPTION = '\n' + f.read()


from circleclient import __version__


setup(
    name='circleclient',
    version=__version__,
    author='Jakub Jarosz',
    author_email='qba73 _at_ postpro.net',
    description='Python client for CircleCI API',
    long_description=LONG_DESCRIPTION,
    url='http://github.com/qba73/circleclient',
    py_modules=['circleclient'],
    license='MIT',
    keywords=['circleci', 'circle', 'ci', 'testing', 'qa'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance'
    ],
)
