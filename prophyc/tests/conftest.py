import sys
import os
import pytest

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, main_dir)

def check_libclang():
    from prophyc.parsers.sack import SackParser
    return SackParser.check()

def pytest_namespace():
    return {
        'clang_installed': pytest.mark.skipif(not check_libclang(), reason = "clang not installed"),
        'clang_not_installed': pytest.mark.skipif(check_libclang(), reason = "clang installed")
    }

@pytest.yield_fixture
def tmpdir_cwd(tmpdir):
    orig_dir = os.getcwd()
    os.chdir(str(tmpdir))
    sys.path.insert(0, str(tmpdir))
    yield tmpdir
    sys.path.pop(0)
    os.chdir(orig_dir)
