#!/usr/bin/env python
"""
Setup script for circleclient.

"""

import os
import sys

from setuptools import setup, find_packages


readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://circleclient.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')


setup(
    name='circleclient',
    version='0.1.6',
    author='Jakub Jarosz',
    author_email='jakub.jarosz@postpro.net',
    description='Python client for CircleCI API',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    url='http://github.com/qba73/circleclient/',
    packages=[
        'circleclient'
    ],
    package_dir={'circleclient': 'circleclient'},
    include_package_data=True,
    install_requires=['requests'],
    license='MIT',
    zip_safe=False,
    keywords=['ci', 'testing', 'qa', 'circleclient'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance'
    ],
)
