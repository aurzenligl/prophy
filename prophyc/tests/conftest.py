import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

@pytest.yield_fixture
def tmpdir_cwd(tmpdir):
    orig_dir = os.getcwd()
    os.chdir(str(tmpdir))
    sys.path.insert(0, str(tmpdir))
    yield tmpdir
    sys.path.pop(0)
    os.chdir(orig_dir)
