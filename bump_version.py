#! /usr/bin/env python

"""
Use this file to bump version in all relevant prophy files when version is incremented:
bump_version.py <NEW_VERSION_NUMBER>
"""

import os
import sys
import re

root = os.path.split(os.path.abspath(__file__))[0]
new_version = sys.argv[1]

def replace(data, format):
    assert 'NUM' in format, "use NUM in format argument of bump function"
    result = re.findall(format.replace('NUM', '(.*)'), data)
    assert len(result) == 1, "there must be exactly one version format match in bumped file"
    return data.replace(format.replace('NUM', result[0]), format.replace('NUM', new_version))

def bump(leaf, format):
    filename = os.path.join(root, leaf)
    assert os.path.exists(filename), "attempted to bump nonexistent file"
    with open(filename, "rb") as f:
        data = f.read()
    data = replace(data, format)
    with open(filename, "wb") as f:
        f.write(data)
    print "bumping {} to {} successful".format(leaf, new_version)

"""
Specify files and version format strings to bump version in.
"""

bump("setup.py", "version = 'NUM',")
bump("prophy/__init__.py", "__version__ = 'NUM'")
bump("prophy/tests/test_version.py", "assert prophy.__version__ == 'NUM'")
bump("prophyc/__init__.py", "__version__ = 'NUM'")
bump("prophyc/tests/test_prophyc.py", "expected_version = b'NUM'")
bump("docs/conf.py", "version = 'NUM'")
bump("docs/conf.py", "release = 'NUM'")
bump("prophy_cpp/wscript", "VERSION = 'NUM'")
