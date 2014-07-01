#!/usr/bin/env python
"""
Setup script for circleclient.

"""

import os
import sys

from distutils.core import setup

this_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_dir, 'README.rst')) as f:
    LONG_DESCRIPTION = '\n' + f.read()


setup(
    name='circleclient',
    version='0.1.1',
    author='Jakub Jarosz',
    author_email='qba73@postpro.net',
    description='Python client for CircleCI API',
    long_description=LONG_DESCRIPTION,
    url='http://github.com/qba73/circleclient/',
    py_modules=['circleclient'],
    license='MIT',
    keywords=['ci', 'testing', 'qa'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance'
    ],
    install_requires=['requests'],
)
