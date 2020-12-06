import os
import re
from setuptools import setup, find_packages


_THIS_DIR = os.path.dirname(__file__)

_VERSION = "3.1.0.dev3"


def _get_long_description():
    with open(os.path.join(_THIS_DIR, "README.rst"), encoding="utf8") as f:
        readme = f.read().strip()
    # PyPI / twine doesn't accept the `raw` directive in reStructuredText.
    long_description = re.sub(
        r"\.\. start-raw-directive[\s\S]+?\.\. end-raw-directive", "", readme
    )
    return long_description


def main():
    setup(
        name="pycantonese",
        version=_VERSION,
        description="PyCantonese: Cantonese Linguistics and NLP in Python",
        long_description=_get_long_description(),
        long_description_content_type="text/x-rst",
        url="https://pycantonese.org",
        project_urls={
            "Bug Tracker": "https://github.com/jacksonllee/pycantonese/issues",
            "Source Code": "https://github.com/jacksonllee/pycantonese",
        },
        download_url="https://pypi.org/project/pycantonese/#files",
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
        install_requires=["pylangacq>=0.12.0,<1.0.0", "wordseg==0.0.2"],
        package_data={
            "pycantonese": [
                "data/hkcancor/*",
                "data/rime_cantonese/*",
                "pos_tagging/*.pickle",
            ],
        },
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
            "Programming Language :: Python :: 3.9",
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
