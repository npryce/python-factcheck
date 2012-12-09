#!/usr/bin/env python

import os
from distutils.core import setup


setup(name='factcheck',
      version='1.0.0.0',
      description='A simple, extensible implementation of QuickCheck for Python',
      author='Nat Pryce',
      author_email='about-factcheck@natpryce.com',
      url='http://github.com/npryce/python-factcheck',
      
      license="Apache 2.0",
      
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Topic :: Software Development :: Testing',
      ],

      provides=['factcheck'],
      py_modules=['factcheck'],
      package_dir={'':'src'}
)
