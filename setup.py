#!/usr/bin/env python

from setuptools import setup
from setuptools.command.test import test as TestCommand
import sys
import os

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_suite = True
        self.test_args = ['test/test_factcheck.py']
        if sys.version_info[0] > 2:
            self.test_args.append('test/test_factcheck_python3.py')
        self.test_args.append('--duration=10')
        
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(name='factcheck',
      version='1.3.0.2',
      description='A simple, extensible implementation of QuickCheck for Python',
      author='Nat Pryce',
      author_email='about-factcheck@natpryce.com',
      url='http://github.com/npryce/python-factcheck',
      
      license="Apache 2.0",
      
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Natural Language :: English',
        'Topic :: Software Development :: Testing',
      ],
      
      provides=['factcheck'],
      py_modules=['factcheck'],
      
      tests_require=['pytest'],
      cmdclass = {'test': PyTest}
)
