# PyCantonese: NLTK-compatible Python module for working with Cantonese corpus data

## Development

Module under development; see the [wiki](https://github.com/pycantonese/pycantonese/wiki) page for work being undertaken.


## Authors

Developer: Jackson L. Lee

In collaboration with Litong Chen and Tsz-Him Tsui for testing and compiling datasets

## Usage

Put the following in the same directory:

- `test_corpus.py`
- `pycantonese.py`
- folder `data_sample` with its contents

Run `test_corpus.py` with Python, and you will see something like this:

    Find all words with a specific tone (e.g., tone 4):
    There are 80 matching words, e.g.:
    直程_zik6cing4
    團_tyun4
    差唔多_caa1m4do1
    長_coeng4
    觀團_gun1tyun4

    Find all words with a specific onset/initial (e.g., 'b'):
    There are 21 matching words, e.g.:
    _beng2
    半_bun3
    邊度_bin1dou6
    _baau1
    避_bei6

    Find all words with a specific nucleus (e.g., 'aa'):
    There are 75 matching words, e.g.:
    吔_jaa3
    差唔多_caa1m4do1
    萬四_maan6sei3
    吖_aa1
    時間_si4gaan3

    Find all words with a specific coda (e.g., 'ng'):
    There are 70 matching words, e.g.:
    直程_zik6cing4
    適應_sik1jing3
    長_coeng4
    興趣_hing3ceoi3
    總之_zung2zi1

    Find all words with a specific final (e.g., 'aan'):
    There are 12 matching words, e.g.:
    聖誕節_sing3daan3zit3
    萬四_maan6sei3
    時間_si4gaan3
    新西蘭_san1sai1laan4
    但_daan6

    *** using a customized function not from PyCantonese ***
    Find all words with a specific coda plus a tone (e.g., 't' and '3'):
    There are 6 matching words, e.g.:
    聖誕節_sing3daan3zit3
    發_faat3
    _daat3
    '\xab\xe6\x9c\x88_baat3jyut6'
    季節_gwai3zit3

    Find all words with a specific character (e.g., '我'):
    There are 3 matching words, e.g.:
    我_ngo5
    我地_ngo5dei6
    我哋_ngo5dei6

    Find all words with a specific character (e.g., '我'),
    each instance with a range -- -2 characters and +3 characters:
    There are 38 instances of '我', e.g.:
    咩_me1
    ？_VQ6
    我_ngo5
    聽_teng1
    朋友_pang4jau5
    講_gong2

    。_VQ1
    但係_daan6hai6
    我_ngo5
    -_VQ2
    係_hai6
    裏邊_leoi5bin6

    呀_aa4
    ，_VQ2
    我_ngo5
    好_hou2
    啲_di1
    喎_wo3


## Data

`data_sample.txt` is derived from KK Luke's Cantonese corpus:

Luke, Kang Kwong. (2011). "The Hong Kong Cantonese corpus: Design and uses". Paper presented at the Roundtable Conference on Linguistic Corpus and Corpus Linguistics in the Chinese Context , The Hong Kong Institute of Education, Hong Kong, May 6-8 2011.
