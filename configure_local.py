import importlib
import sys

import pip

# Fix a bug in python 3.10 and setuptools.
pip.main(["install", "setuptools==59.8.0"])
import _distutils_hack

importlib.reload(_distutils_hack)
import setuptools

importlib.reload(setuptools)

# Install the project dependencies and extras.
from setup import requirements, extra_requirements

pip.main(
    [
        "install",
        *requirements,
        *[
            extra
            for lextras in extra_requirements.values()
            if isinstance(lextras, list)
            for extra in lextras
            if "databricks-connect" not in extra
        ],
    ]
)

from pre_commit.main import main as precommit

sys.argv.append("install")
precommit()
