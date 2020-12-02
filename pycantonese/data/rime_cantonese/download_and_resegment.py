"""This script downloads the rime-cantonese data as JSON files."""

import collections
import io
import json
import logging
import os
import tempfile
import zipfile

from pycantonese.jyutping.parse_jyutping import parse_jyutping
from pycantonese.util import split_characters_with_alphanum


try:
    import requests
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "This script requires the 'requests' package. "
        "Run `pip install requests` and then re-run this script."
    )


_BRANCH = "2020.09.09"
_URL = f"https://github.com/jacksonllee/rime-cantonese/archive/{_BRANCH}.zip"

_THIS_DIR = os.path.abspath(os.path.dirname(__file__))

_DataFile = collections.namedtuple("_DataFile", "yaml_filename, json_filename")
_CHARS_JYUTPING_FILES = (
    _DataFile("jyut6ping3.lettered.dict.yaml", "lettered.json"),
    _DataFile("jyut6ping3.dict.yaml", "chars_to_jyutping.json"),
)
_CHARS_FILES = (
    # Not yet using the "phrases" data.
    # _DataFile("jyut6ping3.phrase.dict.yaml", "phrases.json"),
    # The "maps" data has the Open Data Commons Open Database License (ODbL)
    # that has a share-alike clause -- PyCantonese can't use this data.
    # _DataFile("jyut6ping3.maps.dict.yaml", "maps.json"),
)
_RESEGMENTED_FILENAME = "resegmented.txt"


def _download_chars_jyutping_data(yaml_filename, json_filename):
    chars_to_jyutping_dicts = collections.defaultdict(dict)
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "file.zip")

        with requests.Session() as session, open(zip_path, "wb") as f:
            response = session.get(_URL)
            f.write(response.content)

        with zipfile.ZipFile(zip_path) as zip_file:
            data_path = os.path.join(
                f"rime-cantonese-{_BRANCH}", yaml_filename
            )
            with zip_file.open(data_path) as data_file:
                for line in io.TextIOWrapper(data_file, encoding="utf-8"):
                    line = line.strip()
                    if not line or line.startswith("#") or "\t" not in line:
                        continue

                    parts = line.split("\t")
                    if len(parts) == 2:
                        chars, jyutping = parts
                        # Default frequency is 0.07:
                        # https://github.com/CanCLID/ToJyutping/blob/be4f40d45b9780b3f0e2ffe53eff21df565ffc3f/preprocess.py#L18
                        freq = 0.07
                    elif len(parts) == 3:
                        chars, jyutping, freq_str = parts
                        # Reference for retrieving frequency:
                        # https://github.com/CanCLID/ToJyutping/blob/be4f40d45b9780b3f0e2ffe53eff21df565ffc3f/preprocess.py#L6-L16
                        try:
                            if freq_str.endswith("%"):
                                freq = float(freq_str[:-1]) * 0.01
                            else:
                                freq = float(freq_str)
                        except (ValueError, TypeError):
                            freq = 0.0
                    else:
                        continue

                    jyutping = jyutping.replace(" ", "")
                    chars_to_jyutping_dicts[chars][jyutping] = freq

    chars_to_jyutping = {}

    for chars, jyutping_dict in chars_to_jyutping_dicts.items():
        if len(jyutping_dict) == 1:
            jyutping = list(jyutping_dict.keys())[0]
        else:
            jyutping = sorted(
                jyutping_dict.items(),
                key=lambda x: x[1],  # Targeting the frequency.
                reverse=True,
            )[0][0]
        chars_to_jyutping[chars] = jyutping

    with open(
        os.path.join(_THIS_DIR, json_filename), "w", encoding="utf8"
    ) as f:
        json.dump(chars_to_jyutping, f, indent=4, ensure_ascii=False)


def _download_chars_data(yaml_filename, json_filename):
    chars = []
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "file.zip")

        with requests.Session() as session, open(zip_path, "wb") as f:
            response = session.get(_URL)
            f.write(response.content)

        with zipfile.ZipFile(zip_path) as zip_file:
            data_path = os.path.join(
                f"rime-cantonese-{_BRANCH}", yaml_filename
            )
            with zip_file.open(data_path) as data_file:
                for line in io.TextIOWrapper(data_file, encoding="utf-8"):
                    line = line.strip()
                    if (
                        not line
                        or line.startswith("#")
                        # or line[0].isalpha()
                        or line[0] in "-."
                        or ": " in line
                    ):
                        continue
                    chars.append(line)

    with open(
        os.path.join(_THIS_DIR, json_filename), "w", encoding="utf8"
    ) as f:
        json.dump(chars, f, indent=4, ensure_ascii=False)


def _resegment_chars_jyutping_data(json_filename):
    json_path = os.path.join(_THIS_DIR, json_filename)

    with open(json_path, encoding="utf8") as f:
        chars_to_jyutping = json.load(f)

    with open(
        os.path.join(_THIS_DIR, _RESEGMENTED_FILENAME), encoding="utf8"
    ) as f:
        resegmented = {}
        for line in f:
            line = line.strip()
            if not line or line.startswith("# ") or " " not in line:
                continue
            resegmented[line.replace(" ", "")] = line

    new_chars_to_jyutping = {}

    for chars, jp in chars_to_jyutping.items():
        if chars in resegmented:
            chars_split = split_characters_with_alphanum(chars)
            jp_split = parse_jyutping(jp)

            # Don't bother if we can't match each jyutping syllable
            # with each Cantonese character.
            if len(chars_split) != len(jp_split):
                new_chars_to_jyutping[chars] = jp

            else:
                new_words = resegmented[chars].split()
                i = 0
                for new_word in new_words:

                    # If this new word already exists in the original
                    # mapping, don't re-add it to the new map, or else
                    # we risk altering this word's jyutping representation
                    # (some Cantonese words/characters have multiple
                    # pronunciations, and we've already chosen the more
                    # frequent one according to the rime-cantonese source).
                    if new_word in chars_to_jyutping:
                        i += len(split_characters_with_alphanum(new_word))
                        continue

                    new_jp_for_word = ""
                    for _ in range(
                        len(split_characters_with_alphanum(new_word))
                    ):
                        new_jp_for_word += "".join(jp_split[i])
                        i += 1
                    new_chars_to_jyutping[new_word] = new_jp_for_word
        else:
            new_chars_to_jyutping[chars] = jp

    with open(json_path, "w", encoding="utf8") as f:
        json.dump(new_chars_to_jyutping, f, indent=4, ensure_ascii=False)


def main():
    for f in _CHARS_JYUTPING_FILES:
        logging.info("Downloading %s as %s", f.yaml_filename, f.json_filename)
        _download_chars_jyutping_data(f.yaml_filename, f.json_filename)
        logging.info("Resegmenting %s", f.json_filename)
        _resegment_chars_jyutping_data(f.json_filename)
    for f in _CHARS_FILES:
        logging.info("Downloading %s as %s", f.yaml_filename, f.json_filename)
        _download_chars_data(f.yaml_filename, f.json_filename)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    main()
