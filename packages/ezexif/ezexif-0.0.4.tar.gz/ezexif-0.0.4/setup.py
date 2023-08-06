#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

setup(
    name='ezexif',
    version='0.0.4',
    author='wsgfz',
    author_email='wsgfz.cn@gmail.com',
    url='https://wsgfz.cn',
    description='Wrapper for origin exifread.process_file',
    packages=['ezexif'],
    install_requires=['ExifRead>=2.1.2']
)