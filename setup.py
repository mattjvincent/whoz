#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages

import whoz

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'file2db>=0.9.2',
    'future>=0.15.2',
    'requests>=2.11',
    'intermine>=1.9.6',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='whoz',
    version=whoz.__version__,
    description="Simple API",
    long_description=readme + '\n\n' + history,
    author="Matt Vincent",
    author_email='matt.vincent@jax.org',
    url='https://github.com/mattjvincent/whoz',
    packages=[
        'whoz',
    ],
    package_dir={'whoz':
                 'whoz'},
    entry_points={
        'console_scripts': [
            'whoz=whoz.cli:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='whoz',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
