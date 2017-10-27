import os
import pytest
import subprocess
import sys

import prophyc
from contextlib import contextmanager


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

@pytest.fixture(params=["subprocess", "py_code"])
def call(request, mocker):

    if request.param == "subprocess":

        def call_as_subprocess(call_args):
            popen = subprocess.Popen([sys.executable, "-m", "prophyc"] + call_args,
                                     cwd=main_dir,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            out, err = popen.communicate()
            return popen.returncode, out.decode(), err.decode()

        return call_as_subprocess
    else:
        if request.node.name == "test_sack_parse_warnings[py_code]":
            pytest.xfail("Its not worth of effort to simulate warns comming from source file in this case.")

        if request.node.name == "test_showing_version[py_code]":
            pytest.xfail("It's too tricky to mock sys.stdout.")

        warn_mock = mocker.patch.object(prophyc.Emit, "warn")

        def simulate_Emit_warn(msg):
            return 'prophyc: warning: ' + str(msg) + '\n'

        def call_from_py_code(call_args):

            ret_code = 0
            std_err = ""

            try:
                prophyc.main(call_args)
            except SystemExit as err:
                ret_code = err.code
                if isinstance(ret_code, prophyc.six.string_types):
                    std_err = ret_code + '\n'
                    ret_code = 1

            std_err = ''.join(simulate_Emit_warn(line[0][0]) for line in warn_mock.call_args_list) + std_err
            return ret_code, "", std_err

        return call_from_py_code
