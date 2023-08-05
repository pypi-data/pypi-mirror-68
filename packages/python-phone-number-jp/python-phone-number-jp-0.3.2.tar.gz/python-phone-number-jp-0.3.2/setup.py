#!/usr/bin/env python3
# coding: utf-8
from setuptools import setup
from phone_number_jp import __author__, __version__, __license__

setup(
    name='python-phone-number-jp',
    version=__version__,
    description='Parse Phone numbers of Japan.',
    license=__license__,
    author=__author__,
    author_email='ytyng@live.jp',
    url='https://github.com/torico-tokyo/python-phone-number-jp.git',
    keywords='phone numbers japan.',
    packages=['phone_number_jp'],
    install_requires=[],
    entry_points={},
)
