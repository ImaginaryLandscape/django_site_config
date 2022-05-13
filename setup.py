#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='site_config',
    version='2.0.0',
    description='Django configuration Utility to manage multiple "websites" in a project. ',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    author='Imaginary Landscape',
    author_email='engineering@imagescape.com',
    maintainer='Noel Taylor',
    maintainer_email='ntaylor@imagescape.com',
    install_requires=[
        'django >= 3.2',
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
    ],
)
