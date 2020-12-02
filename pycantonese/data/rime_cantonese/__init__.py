import json
import os


_THIS_DIR = os.path.abspath(os.path.dirname(__file__))

with open(
    os.path.join(_THIS_DIR, "chars_to_jyutping.json"), encoding="utf8"
) as f:
    CHARS_TO_JYUTPING = json.load(f)

with open(os.path.join(_THIS_DIR, "lettered.json"), encoding="utf8") as f:
    LETTERED = json.load(f)
