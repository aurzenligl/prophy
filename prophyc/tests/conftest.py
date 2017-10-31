import os
import pytest
import subprocess
import sys

import prophyc


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

@pytest.yield_fixture
def tmpfiles_cwd(tmpdir_cwd):
    def create_tmp_files(*files_to_create):
        return map(tmpdir_cwd.join, files_to_create)
    yield create_tmp_files

@pytest.fixture
def dummy_file(tmpdir_cwd):
    the_file = tmpdir_cwd.join("input")
    the_file.write('')
    yield str(the_file)


@pytest.fixture
def sys_capture(capsys):

    class Capture(object):
        def __enter__(self):
            capsys.readouterr()
            return self

        def __exit__(self, _, exc_value, __):
            if exc_value:
                sys.stderr.write(str(exc_value) + '\n')
                self.code = 1
            else:
                self.code = 0
            self.out, self.err = capsys.readouterr()
            return True

        def get(self):
            return self.code, self.out, self.err
    return Capture

@pytest.fixture(params=["subprocess", "py_code"])
def call_prophyc(request, sys_capture):
    if request.param == "subprocess":

        def call_as_subprocess(call_args):
            popen = subprocess.Popen([sys.executable, "-m", "prophyc"] + call_args,
                                     cwd=main_dir,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            out, err = popen.communicate()
            return popen.returncode, out.decode(), err.decode()

        return call_as_subprocess

    elif request.param == "py_code":
        def call_captured(call_args):
            with sys_capture() as cp:
                prophyc.main(call_args)
            return cp.get()

        return call_captured
