import sys
import os
import pytest

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, main_dir)

def module_exists(module_name):
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True

clang_installed = pytest.mark.skipif(not module_exists("clang"), reason = "clang not installed")
clang_not_installed = pytest.mark.skipif(module_exists("clang"), reason = "clang installed")

def pytest_namespace():
    return {
        'clang_installed': clang_installed,
        'clang_not_installed': clang_not_installed
    }

@pytest.yield_fixture
def tmpdir_cwd(tmpdir):
    orig_dir = os.getcwd()
    os.chdir(str(tmpdir))
    sys.path.insert(0, str(tmpdir))
    yield tmpdir
    sys.path.pop(0)
    os.chdir(orig_dir)
