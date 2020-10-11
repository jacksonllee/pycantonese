import os
from setuptools import setup, find_packages


_THIS_DIR = os.path.dirname(__file__)
with open(os.path.join(_THIS_DIR, "README.rst")) as f:
    _LONG_DESCRIPTION = f.read().strip()

_VERSION = "2.4.1"


def main():
    setup(
        name="pycantonese",
        version=_VERSION,
        description="PyCantonese",
        long_description=_LONG_DESCRIPTION,
        long_description_content_type="text/x-rst",
        url="http://pycantonese.org/",
        author="Jackson L. Lee",
        author_email="jacksonlunlee@gmail.com",
        license="MIT License",
        packages=find_packages(),
        keywords=[
            "computational linguistics",
            "natural language processing",
            "NLP",
            "Cantonese",
            "linguistics",
            "corpora",
            "speech",
            "language",
            "Chinese",
            "Jyutping",
        ],
        python_requires=">=3.6",
        setup_requires="setuptools>=39",
        install_requires=["pylangacq>=0.10.0,<1.0.0", "wordseg==0.0.1"],
        package_data={"pycantonese": ["data/hkcancor/*"]},
        data_files=[(".", ["README.rst", "LICENSE.txt", "CHANGELOG.md"])],
        zip_safe=False,
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: Science/Research",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: Chinese (Traditional)",
            "Natural Language :: Cantonese",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Topic :: Scientific/Engineering",
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
            "Topic :: Scientific/Engineering :: Human Machine Interfaces",
            "Topic :: Scientific/Engineering :: Information Analysis",
            "Topic :: Text Processing",
            "Topic :: Text Processing :: Filters",
            "Topic :: Text Processing :: General",
            "Topic :: Text Processing :: Indexing",
            "Topic :: Text Processing :: Linguistic",
        ],
    )


if __name__ == "__main__":
    main()
