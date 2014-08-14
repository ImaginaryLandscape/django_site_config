#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='site_config',
      version='0.0.6',
      description='Django configuration Utility to manage multiple "websites" in a project. ',
      long_description=read('README.md'),
      author='Joe Jasinski',
      author_email='jjasinski@imagescape.com',
      install_requires=[
       'django >= 1.6', 
       'jsonfield >= 0.9.22',
      ],
      url='https://github.com/ImaginaryLandscape/django_site_config',
      keywords='django site config configuration',
      extras_require = {
        'testing':  ["mock >= 1.0.1", ],
      },
      classifiers=[
        "Framework :: Django", 
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: BSD License",
      ],
)
