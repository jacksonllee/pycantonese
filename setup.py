# All configurations are set in pyproject.toml only.
# This (dummy) setup.py script is needed for now
# since the chosen build-backend `setuptools` doesn't yet support PEP 660.
# As soon as https://github.com/pypa/setuptools/issues/2816
# is resolved, we can drop this setup.py script entirely.

import setuptools


if __name__ == "__main__":
    setuptools.setup()
