from prophyc import model
from prophyc.generators.cpp import CppGenerator

def generate(nodes):
    return CppGenerator().generate_definitions(nodes)

def test_generate_includes():
    nodes = [model.Include("szydlo"),
             model.Include("mydlo"),
             model.Include("powidlo")]

    assert generate(nodes) == """\
#include "szydlo.hpp"
#include "mydlo.hpp"
#include "powidlo.hpp"
"""

def test_generate_constants():
    nodes = [model.Constant("CONST_A", "0"),
             model.Constant("CONST_B", "31")]

    assert generate(nodes) == """\
enum { CONST_A = 0 };
enum { CONST_B = 31 };
"""

def test_generate_typedefs():
    nodes = [model.Typedef("a", "b")]

    assert generate(nodes) == """\
typedef b a;
"""
