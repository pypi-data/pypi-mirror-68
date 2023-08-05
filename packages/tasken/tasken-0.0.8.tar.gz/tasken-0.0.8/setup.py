#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = "tasken",
    version = "0.0.8",
    description = "task state notify tool",
    long_description = "task state notify tool",
    license = "MIT Licence",
    url = "https://github.com/ChanryLimmy/tasken",
    author = "limmy",
    author_email = "tianqi218@126.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ['requests'],
    python_requires='>=3.6'
)
