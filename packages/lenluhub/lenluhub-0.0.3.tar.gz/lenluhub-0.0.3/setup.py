#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by iFantastic on 2020/5/6


from setuptools import setup, find_packages
from distutils.core import setup
import sys

if sys.version_info < (3, 6):
    sys.exit('Python 3.6 or greater is required.')

with open('README.md', 'r') as fp:
    readme = fp.read()

# 版本号，自己随便写
VERSION = "0.0.3"

LICENSE = "MIT"

setup(
    name='lenluhub',
    version=VERSION,
    description=(
        'lenluhub'
    ),
    long_description=readme,
    author='yangst2',
    author_email='yangst2@lenovo.com',
    maintainer='yanst2',
    maintainer_email='yangst2@lenovo.com',
    license=LICENSE,
    packages=find_packages(),
    url="https://gitlab.lenovo.com/moli",
    platforms=["all"],
    install_requires=[
        "tensorflow==2.1.0",
        "keras==2.3.1",
        "bert4keras==0.7.5",
        "tornado==6.0.4"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries'
    ],
)
