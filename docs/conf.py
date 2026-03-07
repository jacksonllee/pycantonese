# PyCantonese documentation build configuration file, created by
# sphinx-quickstart on Sat Dec 27 15:23:24 2014.

from datetime import date

import pycantonese

# -- General configuration ------------------------------------------------

# Setting this flag is needed to enable the generation of source code pages
# (under "API Reference") and hyperlinks to them.
autosummary_generate = True

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "numpydoc.numpydoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinxcontrib.googleanalytics",
]

# See https://pypi.org/project/sphinx-sitemap/2.2.0/
html_baseurl = "https://pycantonese.org/"
sitemap_url_scheme = "{link}"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'PyCantonese'
author = 'Jackson L. Lee'
html_author_link = author  # can't use the next line?
# html_author_link = '<a href="https://jacksonllee.com/">{}</a>'.format(author)
today_ = date.today()
copyright = f'2014-{date.today().year}, {html_author_link}'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
current_version = pycantonese.__version__

# The short X.Y version.
version = current_version
# The full version, including alpha/beta/rc tags.
release = current_version

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "collapse_navigation": False,
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = "_static/pycantonese-logo-white.svg"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_static/pycantonese-logo.ico"

html_static_path = ['_static']
html_show_sourcelink = False

googleanalytics_id = "UA-181803559"

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ('https://docs.python.org/3/', None),
    "rustling": ("https://rustling.readthedocs.io/stable/", None),
}
