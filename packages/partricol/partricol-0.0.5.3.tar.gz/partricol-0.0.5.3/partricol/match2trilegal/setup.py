#!/usr/bin/env python

from setuptools import setup

setup(
    name='match2trilegal',
    author='Phil Rosenfield',
    author_email='philip.rosenfield@cfa.harvard.edu',
    version='1.0.0b1',
    license='BSD',
    py_modules=['match2trilegal'],
    scripts=['match2trilegal'],
    install_requires=['numpy'],
    url='https://github.com/philrosenfield/match2trilegal'
)
