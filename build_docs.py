#!/usr/bin/env python

"""This script updates the documentation website."""

import logging
import os

import m2r


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))
_DOCS = os.path.join(_THIS_DIR, "docs")
_DOCS_SOURCE = os.path.join(_DOCS, "source")


def remove_generated_docs():
    logging.info("Removing generated docs")
    os.system(f"rm {os.path.join(_DOCS, '*.html')}")
    os.system(f"rm -rf {os.path.join(_DOCS, '_sources')}")
    os.system(f"rm -rf {os.path.join(_DOCS, '_modules')}")
    os.system(f"rm -rf {os.path.join(_DOCS, '_static')}")
    os.system(f"rm -rf {os.path.join(_DOCS, '.doctrees')}")
    os.system(f"rm -rf {os.path.join(_DOCS, '_generated')}")
    os.system(f"rm -rf {os.path.join(_DOCS_SOURCE, '_generated')}")


def rebuild_docs():
    logging.info("Rebuilding docs")
    os.system(f"sphinx-build -b html {_DOCS_SOURCE} {_DOCS}")


def create_changelog_rst():
    logging.info("Creating changelog.rst")
    with open(os.path.join(_THIS_DIR, "CHANGELOG.md")) as f:
        changelog_md = f.read()
    changelog_rst = (
        ".. _changelog:\n\n"
        + "Changelog\n=========\n"
        + m2r.convert(changelog_md[changelog_md.index("## [Unreleased]"):])
    )
    with open(os.path.join(_DOCS_SOURCE, "changelog.rst"), "w") as f:
        f.write(changelog_rst)


def create_robots_txt():
    logging.info("Creating robots.txt")
    with open(os.path.join(_DOCS, "robots.txt"), "w") as f:
        f.write(
            "User-agent: *\n\nSitemap: https://pycantonese.org/sitemap.xml\n"
        )


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    remove_generated_docs()
    rebuild_docs()
    create_changelog_rst()
    create_robots_txt()
