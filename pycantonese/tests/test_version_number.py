import os
import re

import pycantonese
from pycantonese.tests import REPO_DIR


def test_version_number_match_with_changelog():
    """__version__ and CHANGELOG.md match for the latest version number."""
    changelog = open(
        os.path.join(REPO_DIR, "CHANGELOG.md"), encoding="utf-8"
    ).read()
    # latest version number in changelog = the 1st occurrence of '[x.y.z]'
    version_in_changelog = (
        re.search(r"\[\d+\.\d+\.\d+\]", changelog).group().strip("[]")
    )
    assert pycantonese.__version__ == version_in_changelog, (
        "Make sure both __version__ and CHANGELOG are updated to match the "
        "latest version number"
    )
