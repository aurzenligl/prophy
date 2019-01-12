from prophyc import model
from prophyc.generators.python import _PythonTranslator


def serialize(nodes):
    python_translator = _PythonTranslator()
    return python_translator._process_nodes(nodes, "")


def test_includes_rendering():
    nodes = [
        model.Include("szydlo", []),
        model.Include("root/nowe_mydlo", []),
        model.Include("../root/nowiejsze_powidlo", []),
    ]

    ref = """\
from szydlo import *
from nowe_mydlo import *
from nowiejsze_powidlo import *
"""
    assert ref == serialize(nodes)


def test_constants_rendering():
    nodes = [model.Constant("CONST_A", "0", "first constant"),
             model.Constant("CONST_B", "31", "second constant")]

    ref = """\
CONST_A = 0  '''first constant'''
CONST_B = 31  '''second constant'''
"""
    assert ref == serialize(nodes)


def test_typedefs_rendering():
    nodes = [model.Typedef("a", "b")]

    ref = """\
a = b
"""
    assert ref == serialize(nodes)


def test_enums_rendering():
    nodes = [model.Enum("EEnum", [(model.EnumMember("EEnum_A", "0")),
                                  (model.EnumMember("EEnum_B", "1")),
                                  (model.EnumMember("EEnum_C", "2"))])]

    ref = """\
class EEnum(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators = [
        ('EEnum_A', 0),
        ('EEnum_B', 1),
        ('EEnum_C', 2)
    ]

EEnum_A = 0
EEnum_B = 1
EEnum_C = 2
"""
    assert ref == serialize(nodes)


def test_struct_rendering():
    nodes = [model.Struct("Struct", [(model.StructMember("a", "u8")),
                                     (model.StructMember("b", "i64")),
                                     (model.StructMember("c", "r32")),
                                     (model.StructMember("d", "TTypeX"))])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.u8),
        ('b', prophy.i64),
        ('c', prophy.r32),
        ('d', TTypeX)
    ]
"""
    assert ref == serialize(nodes)


def test_struct_rendering_with_dynamic_array():
    nodes = [model.Struct("Struct", [model.StructMember("tmpName", "TNumberOfItems"),
                                     model.StructMember("a", "u8", bound="tmpName")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('tmpName', TNumberOfItems),
        ('a', prophy.array(prophy.u8, bound = 'tmpName'))
    ]
"""
    assert ref == serialize(nodes)


def test_struct_rendering_with_dynamic_arrays_bounded_by_the_same_member():
    nodes = [model.Struct("Struct", [model.StructMember("numOfElements", "TNumberOfItems"),
                                     model.StructMember("tmpName", "u32"),
                                     model.StructMember("a", "u8", bound="numOfElements"),
                                     model.StructMember("b", "r32", bound="numOfElements")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('numOfElements', TNumberOfItems),
        ('tmpName', prophy.u32),
        ('a', prophy.array(prophy.u8, bound = 'numOfElements')),
        ('b', prophy.array(prophy.r32, bound = 'numOfElements'))
    ]
"""
    assert ref == serialize(nodes)


def test_struct_rendering_with_static_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u8", size="NUM_OF_ARRAY_ELEMS")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.array(prophy.u8, size = NUM_OF_ARRAY_ELEMS))
    ]
"""
    assert ref == serialize(nodes)


def test_struct_rendering_with_limited_array():
    nodes = [model.Struct("Struct", [model.StructMember("a_len", "u8"),
                                     model.StructMember("a", "u8", bound="a_len", size="NUM_OF_ARRAY_ELEMS")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a_len', prophy.u8),
        ('a', prophy.array(prophy.u8, bound = 'a_len', size = NUM_OF_ARRAY_ELEMS))
    ]
"""
    assert ref == serialize(nodes)


def test_struct_rendering_with_optional():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u32", optional=True)])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.optional(prophy.u32))
    ]
"""
    assert ref == serialize(nodes)


def test_struct_rendering_with_byte():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.u8)
    ]
"""
    assert ref == serialize(nodes)


def test_struct_rendering_with_byte_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", greedy=True)])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.bytes())
    ]
"""
    assert ref == serialize(nodes)


def test_union_rendering():
    nodes = [model.Union("U", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "B", "1"),
                               model.UnionMember("c", "C", "2")])]

    ref = """\
class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
    _descriptor = [
        ('a', A, 0),
        ('b', B, 1),
        ('c', C, 2)
    ]
"""
    assert ref == serialize(nodes)


def test_union_rendering_2():
    nodes = [model.Union("U", [model.UnionMember("a", "i8", "0"),
                               model.UnionMember("b", "u32", "1"),
                               model.UnionMember("c", "r64", "2")])]

    ref = """\
class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
    _descriptor = [
        ('a', prophy.i8, 0),
        ('b', prophy.u32, 1),
        ('c', prophy.r64, 2)
    ]
"""
    assert ref == serialize(nodes)


def test_python_translator_1():
    ih = []
    th = []
    for x in range(20, 200, 60):
        ih.append(model.Include("test_include_" + str(x), []))
        th.append(model.Typedef("td_elem_name_" + str(x), "td_elem_val_" + str(x)))
        th.append(model.Typedef("td_elem_name_" + str(x), "i_td_elem_val_" + str(x)))
        th.append(model.Typedef("td_elem_name_" + str(x), "u_td_elem_val_" + str(x)))

    enum = []
    for x in range(1, 100, 30):
        enum.append((model.EnumMember("elem_" + str(x), "val_" + str(x))))

    name = "MAC_L2CallConfigResp"
    members = [model.StructMember('messageResult', 'SMessageResult')]
    msg_h = model.Struct(name, members)

    nodes = []
    nodes += ih
    nodes += [model.Constant("C_A", "5"), model.Constant("C_B", "5"), model.Constant("C_C", "C_B + C_A")]
    nodes += th
    nodes += [model.Enum("test", enum)]
    nodes += [msg_h]

    python_translator = _PythonTranslator()
    output = python_translator(nodes, "")

    ref = """\
import prophy

from test_include_20 import *
from test_include_80 import *
from test_include_140 import *

C_A = 5
C_B = 5
C_C = C_B + C_A

td_elem_name_20 = td_elem_val_20
td_elem_name_20 = i_td_elem_val_20
td_elem_name_20 = u_td_elem_val_20
td_elem_name_80 = td_elem_val_80
td_elem_name_80 = i_td_elem_val_80
td_elem_name_80 = u_td_elem_val_80
td_elem_name_140 = td_elem_val_140
td_elem_name_140 = i_td_elem_val_140
td_elem_name_140 = u_td_elem_val_140

class test(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators = [
        ('elem_1', val_1),
        ('elem_31', val_31),
        ('elem_61', val_61),
        ('elem_91', val_91)
    ]

elem_1 = val_1
elem_31 = val_31
elem_61 = val_61
elem_91 = val_91

class MAC_L2CallConfigResp(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('messageResult', SMessageResult)
    ]
"""
    assert output == ref


def test_python_translator_2(larger_model):
    python_translator = _PythonTranslator()
    output = python_translator(larger_model, "")

    assert output == """\
import prophy

a = prophy.i16
c = a

from some_defs import *

class the_union(prophy.with_metaclass(prophy.union_generator, prophy.union)):
    _descriptor = [
        ('a', IncludedStruct, 0),
        ('field_with_a_long_name', Internal, 1),
        ('other', Internal, 4090)
    ]

class E1(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators = [
        ('E1_A', 0),
        ('E1_B_has_a_long_name', 1),
        ('E1_C_desc', 2)
    ]

E1_A = 0
E1_B_has_a_long_name = 1
E1_C_desc = 2

class E2(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators = [
        ('E2_A', 0)
    ]

E2_A = 0

CONST_A = 6
CONST_B = 0

class StructMemberKinds(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('meber_with_no_docstr', prophy.i16),
        ('ext_size', prophy.i16),
        ('optional_element', prophy.optional(Complex)),
        ('fixed_array', prophy.array(Complex, size = 3)),
        ('samples', prophy.array(Complex, bound = 'ext_size')),
        ('limitted_array', prophy.array(prophy.r64, bound = 'ext_size', size = 4)),
        ('greedy', prophy.array(Complex))
    ]
"""
