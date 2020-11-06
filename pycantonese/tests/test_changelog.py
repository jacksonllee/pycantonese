import os

from pycantonese.tests import REPO_DIR


def test_changelog_has_unreleased_section():
    """The 'Unreleased' section is needed to make the doc script work."""
    with open(os.path.join(REPO_DIR, "CHANGELOG.md"), encoding="utf8") as f:
        changelog = f.read()
    assert "\n## [Unreleased]\n" in changelog
