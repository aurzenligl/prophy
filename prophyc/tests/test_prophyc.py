import os
import sys
import subprocess

main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

empty_python_output = """\
import prophy

def bitMaskOr(x, y):
    return x | y

def shiftLeft(x, y):
    return x << y
"""

def tr(str_):
    """ Facilitates testing strings output from windows cmd-line programs. """
    return str_.translate(None, '\r')

def call(args):
    popen = subprocess.Popen(["python", "-m", "prophyc"] + args,
                             cwd = main_dir,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
    out, err = popen.communicate()
    return popen.returncode, out, err

def test_missing_input():
    ret, out, err = call([])
    assert ret == 1
    assert out == ""
    assert tr(err) == "prophyc: error: too few arguments\n"

def test_no_output_directory(tmpdir_cwd):
    open("input.xml", "w").write("")
    ret, out, err = call(["--python_out", "no_dir",
                          os.path.join(str(tmpdir_cwd), "input_xml")])
    assert ret == 1
    assert out == ""
    assert tr(err) == "prophyc: error: argument --python_out: no_dir directory not found\n"

def test_missing_output(tmpdir_cwd):
    open("input.xml", "w")
    ret, out, err = call(["--isar", os.path.join(str(tmpdir_cwd), "input.xml")])
    assert ret == 1
    assert out == ""
    assert tr(err) == "Missing output directives\n"

def test_passing_neither_isar_nor_sack(tmpdir_cwd):
    open("input", "w")
    ret, out, err = call(["--python_out", ".",
                          os.path.join(str(tmpdir_cwd), "input")])
    assert ret == 1
    assert out == ""
    assert tr(err) == "prophyc: error: one of the arguments --isar --sack is required\n"

def test_passing_isar_and_sack(tmpdir_cwd):
    open("input", "w")
    ret, out, err = call(["--isar", "--sack", "--python_out", ".",
                          os.path.join(str(tmpdir_cwd), "input")])
    assert ret == 1
    assert out == ""
    assert tr(err) == "prophyc: error: argument --sack: not allowed with argument --isar\n"

def test_isar_compiles_single_empty_xml(tmpdir_cwd):
    open("input.xml", "w").write("<struct/>")
    ret, out, err = call(["--isar", "--python_out", str(tmpdir_cwd),
                          os.path.join(str(tmpdir_cwd), "input.xml")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert empty_python_output == open("input.py").read()

def test_isar_compiles_multiple_empty_xmls(tmpdir_cwd):
    open("input1.xml", "w").write("<struct/>")
    open("input2.xml", "w").write("<struct/>")
    open("input3.xml", "w").write("<struct/>")
    ret, out, err = call(["--isar",
                          "--python_out",
                          str(tmpdir_cwd),
                          os.path.join(str(tmpdir_cwd), "input1.xml"),
                          os.path.join(str(tmpdir_cwd), "input2.xml"),
                          os.path.join(str(tmpdir_cwd), "input3.xml")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert empty_python_output == open("input1.py").read()
    assert empty_python_output == open("input2.py").read()
    assert empty_python_output == open("input3.py").read()

def test_outputs_to_correct_directory(tmpdir_cwd):
    open("input.xml", "w").write("<struct/>")
    os.mkdir("output")
    ret, out, err = call(["--isar", "--python_out",
                          os.path.join(str(tmpdir_cwd), "output"),
                          os.path.join(str(tmpdir_cwd), "input.xml")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert empty_python_output == open(os.path.join("output", "input.py")).read()

def test_sack_compiles_single_empty_hpp(tmpdir_cwd):
    open("input.hpp", "w").write("")
    ret, out, err = call(["--sack", "--python_out",
                          str(tmpdir_cwd),
                          os.path.join(str(tmpdir_cwd), "input.hpp")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert empty_python_output == open("input.py").read()

def test_isar_patch(tmpdir_cwd):
    open("input.xml", "w").write("""\
<x>
    <struct name="B">
        <member name="a" type="u8"/>
    </struct>
    <struct name="A">
        <member name="a" type="u8"/>
    </struct>
</x>
""")

    open("patch", "w").write("""\
B insert 999 b A
B dynamic b a
""")
    ret, out, err = call(["--isar", "--patch",
                          os.path.join(str(tmpdir_cwd), "patch"),
                          "--python_out",
                          str(tmpdir_cwd),
                          os.path.join(str(tmpdir_cwd), "input.xml")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert empty_python_output + """\

class A(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('a', prophy.u8)]

class B(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('a', prophy.u8),
                   ('b', prophy.array(A, bound = 'a'))]
""" == open("input.py").read()

def test_sack_patch(tmpdir_cwd):
    open("input.hpp", "w").write("""\
struct X
{
    int x;
};
""")
    open("patch", "w").write("""\
X type x r64
""")
    ret, out, err = call(["--sack", "--patch",
                          os.path.join(str(tmpdir_cwd), "patch"),
                          "--python_out", str(tmpdir_cwd),
                          os.path.join(str(tmpdir_cwd), "input.hpp")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert empty_python_output + """\

class X(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('x', prophy.r64)]
""" == open("input.py").read()

def test_isar_cpp(tmpdir_cwd):
    open("input.xml", "w").write("""
<xml>
    <struct name="Test">
        <member name="x" type="u32">
            <dimension isVariableSize="true"/>
        </member>
    </struct>
</xml>
""")

    ret, out, err = call(["--isar",
                          "--cpp_out", str(tmpdir_cwd),
                          os.path.join(str(tmpdir_cwd), "input.xml")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert open("input.hpp").read() == """\
#ifndef _PROPHY_GENERATED_input_HPP
#define _PROPHY_GENERATED_input_HPP

#include <prophy/prophy.hpp>

struct Test
{
    uint32_t x_len;
    uint32_t x[1]; /// dynamic array, size in x_len
};

#endif  /* _PROPHY_GENERATED_input_HPP */
"""

def test_multiple_outputs(tmpdir_cwd):
    open("input.xml", "w").write("""
<xml>
    <struct name="Test">
        <member name="x" type="u32"/>
    </struct>
</xml>
""")

    ret, out, err = call(["--isar",
                          "--python_out", str(tmpdir_cwd),
                          "--cpp_out", str(tmpdir_cwd),
                          os.path.join(str(tmpdir_cwd), "input.xml")])
    assert ret == 0
    assert out == ""
    assert err == ""
    assert open("input.py").read() == """\
import prophy

def bitMaskOr(x, y):
    return x | y

def shiftLeft(x, y):
    return x << y

class Test(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('x', prophy.u32)]
"""
    assert open("input.hpp").read() == """\
#ifndef _PROPHY_GENERATED_input_HPP
#define _PROPHY_GENERATED_input_HPP

#include <prophy/prophy.hpp>

struct Test
{
    uint32_t x;
};

#endif  /* _PROPHY_GENERATED_input_HPP */
"""
