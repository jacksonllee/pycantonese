#!usr/bin/env python3

from setuptools import (setup, find_packages)

setup(name="pycantonese",
    version="1.1-alpha.1",
    description="PyCantonese",

    long_description="""
PyCantonese is a Python library for working with Cantonese corpus data. While it is under active development and many other features and functions are forthcoming, it currently includes JyutPing parsing and conversion tools as well as general search functionalities for built-in or custom corpus data.

Documentation: `http://pycantonese.org/ <http://pycantonese.org/>`_
""",

    url="http://pycantonese.org/",
    author="Jackson Lee",
    author_email="jsllee.phon@gmail.com",
    license="Apache License, Version 2.0",
    packages=find_packages(),
    keywords=['computational linguistics', 'natural language processing',
                'NLP', 'Cantonese', 'linguistics', 'corpora', 'speech',
                'language', 'Chinese', 'Jyutping', 'NLTK', 'tagging'],
    install_requires=["nltk"],

    package_data={
        "pycantonese": ["data/hkcancor/*"],
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
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Text Processing :: General',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic'
    ],
)

