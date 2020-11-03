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


def insert_social_media_links():
    logging.info("Inserting social media links")
    social_media_html = """
<div id="fb-root"></div>
<script async defer crossorigin="anonymous" src="https://connect.facebook.net/en_US/sdk.js#xfbml=1&version=v8.0" nonce="4Dv3gcYx"></script>
<div class="fb-page" data-href="https://www.facebook.com/pycantonese/" data-tabs="timeline" data-width="" data-height="" data-small-header="true" data-adapt-container-width="true" data-hide-cover="false" data-show-facepile="true">
    <blockquote cite="https://www.facebook.com/pycantonese/" class="fb-xfbml-parse-ignore"><a href="https://www.facebook.com/pycantonese/">PyCantonese: Cantonese Linguistics and NLP in Python</a></blockquote>
</div>
"""  # noqa: E501
    index_html_path = os.path.join(_DOCS, "index.html")
    with open(index_html_path) as f:
        index_html = f.read()
    index_html = index_html.replace("#social-media#", social_media_html)
    with open(index_html_path, "w") as f:
        f.write(index_html)


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    remove_generated_docs()
    rebuild_docs()
    create_changelog_rst()
    insert_social_media_links()
