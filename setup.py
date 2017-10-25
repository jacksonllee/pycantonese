from os import path
from setuptools import setup, find_packages

THIS_DIR = path.dirname(__file__)

with open(path.join(THIS_DIR, 'pycantonese', 'VERSION')) as f:
    package_version = f.read().strip()

with open(path.join(THIS_DIR, 'README.rst')) as f:
    long_description = f.read().strip()


def main():
    setup(name='pycantonese',
          version=package_version,
          description='PyCantonese',
          long_description=long_description,
          url='http://pycantonese.org/',
          author='Jackson Lee',
          author_email='jacksonlunlee@gmail.com',
          license='MIT License',
          packages=find_packages(),
          keywords=['computational linguistics', 'natural language processing',
                    'NLP', 'Cantonese', 'linguistics', 'corpora', 'speech',
                    'language', 'Chinese', 'Jyutping', 'tagging'],

          install_requires=['pylangacq'],

          package_data={
              'pycantonese': ['data/hkcancor/*', 'VERSION'],
          },

          zip_safe=False,

          classifiers=[
              'Development Status :: 5 - Production/Stable',
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
