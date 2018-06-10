import os
from setuptools import setup, find_packages


_THIS_DIR = os.path.dirname(__file__)

with open(os.path.join(_THIS_DIR, 'README.rst')) as f:
    _LONG_DESCRIPTION = f.read().strip()

__version__ = None  # updated in the next line
exec(open(os.path.join(_THIS_DIR, 'pycantonese', '_version.py')).read())
assert __version__ is not None


def main():
    setup(name='pycantonese',
          version=__version__,
          description='PyCantonese',
          long_description=_LONG_DESCRIPTION,
          url='http://pycantonese.org/',
          author='Jackson Lee',
          author_email='jacksonlunlee@gmail.com',
          license='MIT License',
          packages=find_packages(),
          keywords=['computational linguistics', 'natural language processing',
                    'NLP', 'Cantonese', 'linguistics', 'corpora', 'speech',
                    'language', 'Chinese', 'Jyutping', 'tagging'],

          install_requires=[
              'pylangacq>=0.10.0'
          ],

          package_data={
              'pycantonese': ['data/hkcancor/*'],
          },

          zip_safe=False,

          classifiers=[
              'Development Status :: 4 - Beta',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'Intended Audience :: Education',
              'Intended Audience :: Information Technology',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: MIT License',
              'Natural Language :: Chinese (Traditional)',
              'Natural Language :: Cantonese',
              'Operating System :: OS Independent',
              'Programming Language :: Python :: 3',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
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


if __name__ == '__main__':
    main()
