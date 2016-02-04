#!usr/bin/env python3
# -*- coding: utf-8 -*-

from os import path
import sys
from setuptools import (setup, find_packages)

py_version = sys.version_info[:2]
if py_version < (3, 4):
    sys.exit('Error: PyCantonese requires Python 3.4 or above.\n'
             'You are using Python {}.{}.'.format(*py_version))

if __name__ == '__main__':
    version_fname = 'VERSION_DEV'
else:
    version_fname = 'VERSION'

version_path = path.join(path.dirname(__file__), 'pycantonese', version_fname)
with open(version_path) as f:
    package_version = f.read().strip()

setup(name='pycantonese',
      version=package_version,
      description='PyCantonese',
      long_description='PyCantonese: Cantonese Linguistics in Python',
      url='http://pycantonese.org/',
      author='Jackson Lee',
      author_email='jsllee.phon@gmail.com',
      license='Apache License, Version 2.0',
      packages=find_packages(),
      keywords=['computational linguistics', 'natural language processing',
                'NLP', 'Cantonese', 'linguistics', 'corpora', 'speech',
                'language', 'Chinese', 'Jyutping', 'tagging'],

      install_requires=['pylangacq'],

      package_data={
          'pycantonese': ['data/hkcancor/*', 'VERSION', 'VERSION_DEV'],
      },

      zip_safe=False,

      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Natural Language :: Chinese (Traditional)',
          'Natural Language :: Cantonese',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing',
          'Topic :: Text Processing :: Filters',
          'Topic :: Text Processing :: General',
          'Topic :: Text Processing :: Indexing',
          'Topic :: Text Processing :: Linguistic',
          ],
      )
