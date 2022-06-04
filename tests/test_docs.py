"""Tests related to the documentation."""


import pytest
import requests


@pytest.mark.parametrize(
    "url",
    [
        "https://talkbank.org/manuals/CHAT.pdf",
        "https://pylangacq.org/",
        "http://compling.hss.ntu.edu.sg/hkcancor/",
        "https://github.com/jacksonllee/pycantonese/blob/main/src/pycantonese/data/hkcancor/README.md",  # noqa: E501
        "https://childes.talkbank.org/data/Biling/YipMatthews.zip",
        "https://pylangacq.org/read.html",
        "https://pylangacq.org/headers.html",
        "https://docs.python.org/3/library/re.html",
        "https://www.lshk.org/jyutping",
        "https://www.tug.org/TUGboat/tb17-2/tb51rei.pdf",
        "https://universaldependencies.org/u/pos/index.html",
        "https://pycantonese.org/index.html#links",
        # Archives
        "https://pycantonese.org/papers/lee-chen-tsui-wicl3-slides-2016-03-12.pdf",
        "https://pycantonese.org/papers/lee-chen-tsui-wicl3-handout-2016-03-12.pdf",
        "https://pycantonese.org/papers/Lee-pycantonese-2015.html",
        "https://github.com/jacksonllee/pycantonese/blob/main/docs/tutorials/lee-pycantonese-2021-05-16.ipynb",  # noqa: E501
        "https://github.com/jacksonllee/pycantonese/blob/main/docs/tutorials/lee-python-2021-april.ipynb",  # noqa: E501
        "https://github.com/chaaklau/school-of-cantonese-2021-materials/blob/main/chaak_sfp_2021_05_16.ipynb",  # noqa: E501
        "https://github.com/charlestklam/school-of-cantonese-studies-2021/blob/main/Multiword_Expressions_Discontinuous_Constructions.ipynb",  # noqa: E501
        "https://jacksonllee.com/papers/pycantonese_lrec_2022-05-06.pdf",
        "https://github.com/jacksonllee/pycantonese/blob/main/docs/tutorials/lee-cantonese-childes-2022-05-27.ipynb",  # noqa: E501
    ],
)
def test_urls_work(url):
    """URLs used in the documentation shouldn't be dead."""
    with requests.get(url) as r:
        assert r.status_code == 200
