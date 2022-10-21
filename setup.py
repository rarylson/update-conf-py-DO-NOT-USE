"""update-conf.py setup.py file
"""

import os
from os.path import abspath, dirname, join, isfile
import shutil
from distutils import log
from setuptools import setup, Command
from setuptools.command.egg_info import egg_info
from setuptools.command.install import install

from update_conf_py import main

# Consts
GITHUB_URL = "https://github.com/rarylson/update-conf.py"
README_MD = "README.md"
README_RST = "README.rst"

# Important vars
cur_dir = abspath(dirname(__file__))
readme_md = join(cur_dir, README_MD)
readme_rst = join(cur_dir, README_RST)
sample_config = join("samples", main.CONFIG_NAME)
# Get description from the first line of the module docstring.
description = main.__doc__.split('\n')[0]
# Get the long description from the 'README.rst' file (if it exists). Else,
# fallback to the module docstring.
# 'README.rst' MUST be required when generating dists or registering to PyPI.
# In all the other cases, it's fine to use the module docstring.
long_description = ""
using_rst = False
try:
    with open(readme_rst, 'r') as f:
        long_description = f.read()
        using_rst = True
except IOError:
    long_description = main.__doc__
# Env vars for workaround
using_check_manifest = os.environ.get('CHECK_MANIFEST', None) == 'True'


class GenerateRstCommand(Command):
    """Generate a README.rst file

    This file can be used after in the register command.
    """

    description = "generate a README.rst file from README.md"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        if isfile(readme_rst):
            os.remove(readme_rst)

    def run(self):
        import tempfile
        import shutil
        import re

        import pypandoc

        tmp_readme_md = join(tempfile.gettempdir(), README_MD)
        shutil.copy(readme_md, tmp_readme_md)
        try:
            with open(tmp_readme_md, "r") as f:
                md = f.read()
            # Convert links that points to a relative URL
            # The markdown file may be relative URLs (like [Page](page)).
            # However, we do not want these links in Pypi (they will be
            # broken). We want to replace them by absolutive URLs (like
            # [Page]({url}/blob/master/page)).
            # For now, the conversions are hardcoded.
            md_link_re = r"\(LICENSE\)"
            md_link_new = r"({0}/blob/master/LICENSE)".format(GITHUB_URL)
            new_md = re.sub(md_link_re, md_link_new, md)
            md_link_re = r"\(CHANGELOG\.md\)"
            md_link_new = r"({0}/blob/master/CHANGELOG.md)".format(GITHUB_URL)
            new_md = re.sub(md_link_re, md_link_new, new_md)
            with open(tmp_readme_md, "w") as f:
                f.write(new_md)
            # Now, convert to RST
            rst = pypandoc.convert_file(tmp_readme_md, "rst")
            with open(readme_rst, "w") as f:
                f.write(rst)
        finally:
            os.remove(tmp_readme_md)


class EggInfoCommand(egg_info):
    """Check if we're using README.rst before registering in PyPI or before
    creating dists

    This is necessary to avoid uploading packages / registring versions without
    the correct 'long_description'.
    """

    def finalize_options(self):
        if (any(x in self.distribution.commands for x in
                ["register", "sdist", "bdist_wheel"]) and
                not using_check_manifest):
            if not using_rst:
                raise Exception("{} file not found".format(README_RST))

        return egg_info.finalize_options(self)


# Setup
setup(
    # Main software info
    name=main.__program__,
    version=main.__version__,
    description=description,
    long_description=long_description,
    license=main.__license__,
    author=main.__author__,
    author_email=main.__email__,
    url=GITHUB_URL,
    download_url="{0}/tarball/{1}".format(GITHUB_URL, main.__version__),
    keywords="system unix config split snippets sysadmin",
    packages=["update_conf_py"],

    # Requirements
    setup_requires=[
        "setuptools>=0.8",
    ],
    tests_require=[
        "setuptools>=0.8",
        "unittest2>=1.0.0",
    ],

    # Classifiers
    # See: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: System :: Systems Administration",
        "Topic :: Utilities",
    ],

    # Entry points
    # The script itself is defined here.
    entry_points={
        "console_scripts": [
            "update-conf.py = update_conf_py:run",
        ],
    },

    # Data files
    data_files=[
        (join("share", main.__program__), [sample_config, ]),
    ],

    # Tests
    test_suite="tests",

    # Commands
    cmdclass={
        "generate_rst": GenerateRstCommand,
        "egg_info": EggInfoCommand,
    }
)
