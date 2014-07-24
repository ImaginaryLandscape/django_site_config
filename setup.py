#!/usr/bin/env python

from setuptools import setup

setup(name='site_config',
      version='0.0.1',
      description='istribution Utilities',
      author='Joe Jasinski',
      author_email='jjasinski@imagesape.com',
      install_requires=[
       'django >= 1.6', 
       'jsonfield>=0.9.22',
      ],
      extras_require = {
        'testing':  ["mock >= 1.0.1", ],
     }      
)
