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
with open(os.path.join(this_dir, 'README.md')) as f:
    LONG_DESCRIPTION = '\n' + f.read()


from circleclient import __version__


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


setup(
    name='circleclient',
    version='0.1.0',
    description='Python client for CircleCI API',
    long_description=LONG_DESCRIPTION,
    author='Jakub Jarosz',
    author_email='qba73 _at_ postpro.net',
    url='https://github.com/qba73/circleclient',
    py_modules=['circleclient'],
    license='Apache v2.0',
    keywords='circleci ci testing',
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
