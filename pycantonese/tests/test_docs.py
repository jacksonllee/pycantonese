"""Tests related to the documentation."""


import pytest
import requests


@pytest.mark.parametrize(
    "url",
    [
        "https://talkbank.org/manuals/CHAT.pdf",
        "https://pylangacq.org/",
        "http://compling.hss.ntu.edu.sg/hkcancor/",
        "https://github.com/jacksonllee/pycantonese/blob/master/pycantonese/data/hkcancor/README.md",  # noqa: E501
        "https://childes.talkbank.org/data/Biling/YipMatthews.zip",
        "https://pylangacq.org/read.html",
        "https://pylangacq.org/headers.html",
        "https://docs.python.org/3/library/re.html",
        "https://www.lshk.org/jyutping",
        "https://www.ctan.org/pkg/tipa?lang=en",
        "https://pycantonese.org/papers/lee-chen-tsui-wicl3-slides-2016-03-12.pdf",
        "https://pycantonese.org/papers/lee-chen-tsui-wicl3-handout-2016-03-12.pdf",
        "https://pycantonese.org/papers/Lee-pycantonese-2015.html",
        "https://universaldependencies.org/u/pos/index.html",
        "https://pycantonese.org/index.html#links",
    ],
)
def test_urls_work(url):
    """URLs used in the documentation shouldn't be dead."""
    with requests.get(url) as r:
        assert r.status_code == 200
