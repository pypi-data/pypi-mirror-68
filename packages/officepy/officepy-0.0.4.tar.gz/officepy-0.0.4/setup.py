
"""Module Setup"""

import runpy
import os
from setuptools import setup, find_packages

PACKAGE_NAME = "officepy"
here = os.path.dirname(os.path.abspath(__file__))
version_meta = runpy.run_path(os.path.join(here, "version.py"))
VERSION = version_meta["__version__"]

with open(os.path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(os.path.join(here, filename)))
    return [line for line in lineiter if line and not line.startswith("#")]

if __name__ == "__main__":
    setup(
        name = PACKAGE_NAME,
        version = VERSION,
        packages = find_packages(),
        install_requires=parse_requirements("requirements.txt"),
        python_requires=">=3.6.3",
        description="Office Python API",
        long_description=long_description,
        long_description_content_type="text/markdown",
        include_package_data = True,
        data_files = [
        ('share/jupyter/nbextensions/officepy', [
            'officepy/nbextension/static/extension.js'
        ],),
        # classic notebook extension
        ('etc/jupyter/nbconfig/notebook.d' ,[
            'officepy/nbextension/officepy.json'
        ]),
        # server extension
        ('etc/jupyter/jupyter_notebook_config.d', [
            'officepy/nbserver_extension/officepy.json'
        ]),
        ],
        author="Office Dev",
        author_email="officepy@microsoft.com",
        url="https://github.com/officedev"
        )