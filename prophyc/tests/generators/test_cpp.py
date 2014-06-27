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

def test_generate_enums():
    nodes = [model.Enum("EEnum", [model.EnumMember("EEnum_A", "0"),
                                  model.EnumMember("EEnum_B", "1"),
                                  model.EnumMember("EEnum_C", "2")])]

    assert generate(nodes) == """\
enum EEnum
{
    EEnum_A = 0,
    EEnum_B = 1,
    EEnum_C = 2
};
"""

def test_generate_struct():
    nodes = [model.Struct("Struct", [(model.StructMember("a", "u8", None, None, None, False)),
                                     (model.StructMember("b", "i64", None, None, None, False)),
                                     (model.StructMember("c", "r32", None, None, None, False)),
                                     (model.StructMember("d", "TTypeX", None, None, None, False))])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a;
    int64_t b;
    float c;
    TTypeX d;
};
"""

def test_generate_struct_with_dynamic_array():
    nodes = [model.Struct("Struct", [model.StructMember("tmpName", "TNumberOfItems", None, None, None, False),
                                     model.StructMember("a", "u8", True, "tmpName", None, False)])]

    assert generate(nodes) == """\
struct Struct
{
    TNumberOfItems tmpName;
    uint8_t a[1]; /// dynamic array, size in tmpName
};
"""

def test_generate_struct_with_fixed_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u8", True, None, "NUM_OF_ARRAY_ELEMS", False)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a[NUM_OF_ARRAY_ELEMS];
};
"""

def test_generate_struct_with_limited_array():
    nodes = [model.Struct("Struct", [model.StructMember("a_len", "u8", None, None, None, False),
                                     model.StructMember("a", "u8", True, "a_len", "NUM_OF_ARRAY_ELEMS", False)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a_len;
    uint8_t a[NUM_OF_ARRAY_ELEMS]; /// limited array, size in a_len
};
"""

def test_generate_struct_with_byte():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", False, None, None, None)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a;
};
"""

def test_generate_struct_with_byte_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", True, None, None, None)])]

    assert generate(nodes) == """\
struct Struct
{
    uint8_t a[1]; /// greedy array
};
"""
