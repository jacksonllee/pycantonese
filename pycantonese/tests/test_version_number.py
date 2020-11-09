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
    if "dev" in pycantonese.__version__:
        # CHANGELOG.md doesn't update the section headings for dev versions,
        # and so pycantonese.__version__ with "dev" (e.g., "3.1.0dev1")
        # wouldn't match any version headings in CHANGELOG.md.
        return
    assert pycantonese.__version__ == version_in_changelog, (
        "Make sure both __version__ and CHANGELOG are updated to match the "
        "latest version number"
    )
