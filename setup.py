#!/usr/bin/env python

from setuptools import setup

setup(name='site_config',
      version='0.0.3',
      description='Django configuration Utility to manage multiple "websites" in a project. ',
      author='Joe Jasinski',
      author_email='jjasinski@imagescape.com',
      install_requires=[
       'django >= 1.6', 
       'jsonfield >= 0.9.22',
      ],
      extras_require = {
        'testing':  ["mock >= 1.0.1", ],
     }      
)
