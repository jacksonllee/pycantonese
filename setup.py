from setuptools import setup

setup(name='pycantonese',
    version='0.1',
    description='Working with Cantonese corpus data using Python',
    url='http://pycantonese.github.io/',
    author='Jackson L. Lee',
    author_email='jsllee.phon@gmail.com',
    license='Apache',
    packages=['pycantonese'],
    install_requires=['nltk'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Chinese (Traditional)',
#        'Natural Language :: Cantonese',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Scientific/Engineering',
        'Topic :: Text Processing :: Linguistic'
    ]

)
