"""Tests related to the documentation."""

import warnings

import pytest
import requests


@pytest.mark.parametrize(
    "url",
    [
        "https://talkbank.org/",
        "https://talkbank.org/0info/manuals/CHAT.pdf",
        "https://childes.talkbank.org/access/Biling/CHCC.html",
        "https://childes.talkbank.org/access/Biling/Guthrie.html",
        "https://childes.talkbank.org/access/Chinese/Cantonese/HKU.html",
        "https://childes.talkbank.org/access/Chinese/Cantonese/LeeWongLeung.html",
        "https://talkbank.org/childes/access/Biling/EACMC.html",
        "https://childes.talkbank.org/access/Biling/YipMatthews.html",
        "https://pylangacq.org/",
        "https://docs.pylangacq.org/stable/read.html",
        "https://pylangacq.org/read.html",
        "https://pylangacq.org/headers.html",
        "https://docs.python.org/3/library/re.html",
        "https://lshk.org/jyutping-scheme/",
        "https://www.ctan.org/pkg/tipa?lang=en",
        "https://universaldependencies.org/u/pos/index.html",
        # "https://docs.pycantonese.org/index.html#links",
        # Archives
        # "https://docs.pycantonese.org/papers/lee-chen-tsui-wicl3-slides-2016-03-12.pdf",
        # "https://docs.pycantonese.org/papers/lee-chen-tsui-wicl3-handout-2016-03-12.pdf",  # noqa: E501
        # "https://docs.pycantonese.org/papers/Lee-pycantonese-2015.html",
        "https://jacksonllee.com/papers/pycantonese_lrec_2022-05-06.pdf",
    ],
)
def test_urls_work(url):
    """URLs used in the documentation shouldn't be dead."""
    with requests.get(url) as r:
        assert r.status_code == 200


@pytest.mark.parametrize(
    "url",
    [
        "https://github.com/fcbond/hkcancor",
        "https://github.com/jacksonllee/pycantonese/blob/main/src/pycantonese/data/hkcancor/README.md",  # noqa: E501
        "https://github.com/jacksonllee/pycantonese/blob/main/docs/tutorials/lee-pycantonese-2021-05-16.ipynb",  # noqa: E501
        "https://github.com/jacksonllee/pycantonese/blob/main/docs/tutorials/lee-python-2021-april.ipynb",  # noqa: E501
        "https://github.com/chaaklau/school-of-cantonese-2021-materials/blob/main/chaak_sfp_2021_05_16.ipynb",  # noqa: E501
        "https://github.com/charlestklam/school-of-cantonese-studies-2021/blob/main/Multiword_Expressions_Discontinuous_Constructions.ipynb",  # noqa: E501
        "https://github.com/jacksonllee/pycantonese/blob/main/docs/tutorials/lee-cantonese-childes-2022-05-27.ipynb",  # noqa: E501
        "https://gist.github.com/chaaklau/74444ef3b0c56c720148b730025fd57f",
    ],
)
def test_github_urls_work(url):
    """GitHub URLs used in the documentation shouldn't be dead."""
    with requests.get(url) as r:
        if r.status_code == 429:
            warnings.warn(f"Rate limited by GitHub: {url}")
            return
        assert r.status_code == 200
