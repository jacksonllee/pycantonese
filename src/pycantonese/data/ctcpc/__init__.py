import json
import os

_THIS_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_THIS_DIR, "sents.json"), encoding="utf8") as f:
    SENTS = json.load(f)
