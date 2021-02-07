#!/usr/bin/env python
from __future__ import absolute_import
import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='site_config',
    version='1.0.1',
    description='Django configuration Utility to manage multiple "websites" in a project. ',
    long_description=read('README.md'),
    author='Joe Jasinski',
    author_email='jjasinski@imagescape.com',
    install_requires=[
        'django >= 1.11',
        'jsonfield >= 0.9.22',
    ],
    url='https://github.com/ImaginaryLandscape/django_site_config',
    keywords='django site config configuration',
    extras_require={
        'testing': ["mock >= 1.0.1", "six >= 1.9.0"],
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Framework :: Django",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
    ],
)
