import pytest
import sys
import os

main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
prophyc_dir = os.path.join(main_dir, "prophyc")

sys.path.append(main_dir)
sys.path.append(prophyc_dir)

@pytest.yield_fixture
def tmpdir_cwd(tmpdir):
    orig_dir = os.getcwd()
    os.chdir(str(tmpdir))
    sys.path.insert(0, str(tmpdir))
    yield tmpdir
    sys.path.pop(0)
    os.chdir(orig_dir)
