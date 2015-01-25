from setuptools import setup

setup(name='pycantonese',
    version='0.2.1',
    description='Working with Cantonese corpus data using Python',
    url='http://pycantonese.github.io/',
    author='Jackson L. Lee',
    author_email='jsllee.phon@gmail.com',
    license='MIT',
    packages=['pycantonese'],
    keywords=['computational linguistics', 'natural language processing', 'NLP',
              'Cantonese', 'linguistics', 'corpora', 'speech', 'language',
              'Chinese', 'Jyutping', 'NLTK'],
    install_requires=['nltk'],

    package_data={
        'pycantonese': ['data/luke/*'],
    },

    zip_safe=False,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: Cantonese',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic'
    ],
)

