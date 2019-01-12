import os
import subprocess
import sys

import pytest

import prophyc
from prophyc import model, six

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
sys.path.insert(0, main_dir)


def pytest_assertrepr_compare(op, left, right):
    """
    It's quite common that we compare string representation of documents.
    Native pytest's comparison failure representation is at least unreadable for this purpose.
    This prints compared strings only in case of test's failure.
    """
    if op == "==" and isinstance(left, six.string_types) and isinstance(right, six.string_types):
        if len(left) > 60 or len(right) > 60:
            print("--- (left):")
            print(left)
            print("---")
            print("does not match currently defined reference:")
            print("--- (right):")
            print(right)
            print("---")


def check_libclang():
    from prophyc.parsers.sack import SackParser
    return SackParser.check()


@pytest.fixture
def if_clang_installed():
    result = check_libclang()
    if not result:
        pytest.skip("clang not installed")
    return result


@pytest.fixture
def if_clang_not_installed():
    result = check_libclang()
    if result:
        pytest.skip("clang installed")
    return result


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


@pytest.fixture(params=["py_code"])
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


@pytest.fixture
def lorem_with_breaks():
    return "\n".join([
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
        "ut labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan "
        "lacus vel facilisis:",
        "  - Dui ut ornare,",
        "  - Lectus,",
        "  - Malesuada pellentesque,",
        "",
        "",
        "Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas sed.",
        "Egestas integer eget aliquet.",
    ])


@pytest.fixture
def larger_model(lorem_with_breaks):
    return [
        model.Typedef('a', 'i16'),
        model.Typedef('c', 'a'),
        model.Include('some_defs', [
            model.Struct('IncludedStruct', [
                model.StructMember('member1', 'c', 'doc for member1'),
                model.StructMember('member2', 'u32', 'docstring for member1')
            ]),
            model.Typedef('c', 'a'),
        ]),
        model.Union('the_union', [
            model.UnionMember('a', 'IncludedStruct', 0),
            model.UnionMember('field_with_a_long_name', 'Internal', 1, docstring='defined internally'),
            model.UnionMember('other', 'Internal', 4090, docstring='This one has longer discriminator'),
        ], "spec for that union"),
        model.Enum('E1', [
            model.EnumMember('E1_A', '0', 'enum1 constant value A'),
            model.EnumMember('E1_B_has_a_long_name', '1', 'enum1 constant va3lue B'),
            model.EnumMember('E1_C_desc', '2', lorem_with_breaks[:150]),
        ], "Enumerator is a model type that is not supposed to be serialized. Its definition represents yet another "
           "syntax variation for typing a constant. Of course elements of it's type are serializable "
           "(as int32)"),
        model.Enum('E2', [
            model.EnumMember('E2_A', '0', "Short\nmultiline\ndoc"),
        ]),
        model.Constant('CONST_A', '6'),
        model.Constant('CONST_B', '0'),
        model.Struct('StructMemberKinds', [
            model.StructMember('meber_with_no_docstr', 'i16'),
            model.StructMember('ext_size', 'i16', docstring='arbitrary sizer for dynamic arrays'),
            model.StructMember('optional_element', 'Complex', optional=True, docstring='optional array'),
            model.StructMember('fixed_array', 'Complex', size=3, docstring='Array with static size.'),
            model.StructMember('samples', 'Complex', bound='ext_size', docstring='dynamic (ext.sized) array'),
            model.StructMember('limitted_array', 'r64', size=4, bound='ext_size', docstring='Has statically '
                                                                                            'evaluable maximum size.'),
            model.StructMember('greedy', 'Complex', greedy=True, docstring='Represents array of arbitrary '
                                                                           'number of elements. Buffer size '
                                                                           'must be multiply of element size.'),
        ], lorem_with_breaks[:400]),
    ]
