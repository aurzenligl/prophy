from prophyc import model
from prophyc.generators.python import _PythonTranslator


def serialize(nodes):
    python_translator = _PythonTranslator()
    return python_translator._process_nodes(nodes, "")


def test_includes_rendering():
    common_include = model.Include("foo", [
        model.Constant("symbol_1", 1),
        model.Constant("number_12", 12),
    ])
    nodes = [
        common_include,
        model.Include("root/ni_knights", [
            model.Include("../root/rabbit", [
                common_include,
                model.Constant("pi", "3.14159"),
                model.Typedef("definition", "things", "r32", "docstring"),
            ]),
            model.Constant("symbol_2", 2),
        ]),
        model.Include("../root/baz_bar", []),
        model.Include("many/numbers", [model.Constant("number_%s" % n, n) for n in reversed(range(20))]),
    ]

    ref = """\
from foo import number_12, symbol_1
from ni_knights import definition, pi, symbol_2
from numbers import (
    number_0, number_1, number_10, number_11, number_13, number_14, number_15,
    number_16, number_17, number_18, number_19, number_2, number_3, number_4,
    number_5, number_6, number_7, number_8, number_9
)
"""
    # call twice to check if 'duplication avoidance' machinery in _PythonTranslator.translate_include works ok
    assert serialize(nodes) == ref
    assert serialize(nodes) == ref


def test_constants_rendering():
    nodes = [model.Constant("CONST_A", "0", "first constant"),
             model.Constant("CONST_B", "31", "second constant")]

    ref = """\
'''first constant'''
CONST_A = 0
'''second constant'''
CONST_B = 31
"""
    assert serialize(nodes) == ref


def test_typedefs_rendering():
    nodes = [model.Typedef("a", "b")]

    ref = """\
a = b
"""
    assert serialize(nodes) == ref


def test_enums_rendering():
    nodes = [model.Enum("EEnum", [(model.EnumMember("EEnum_A", "0")),
                                  (model.EnumMember("EEnum_B", "1")),
                                  (model.EnumMember("EEnum_C", "2"))])]

    ref = """\
class EEnum(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators = [
        ('EEnum_A', 0),
        ('EEnum_B', 1),
        ('EEnum_C', 2),
    ]


EEnum_A = 0
EEnum_B = 1
EEnum_C = 2
"""
    assert serialize(nodes) == ref


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
        ('d', TTypeX),
    ]
"""
    assert serialize(nodes) == ref


def test_struct_rendering_with_dynamic_array():
    nodes = [model.Struct("Struct", [model.StructMember("tmpName", "TNumberOfItems"),
                                     model.StructMember("a", "u8", bound="tmpName")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('tmpName', TNumberOfItems),
        ('a', prophy.array(prophy.u8, bound='tmpName')),
    ]
"""
    assert serialize(nodes) == ref


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
        ('a', prophy.array(prophy.u8, bound='numOfElements')),
        ('b', prophy.array(prophy.r32, bound='numOfElements')),
    ]
"""
    assert serialize(nodes) == ref


def test_struct_rendering_with_static_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u8", size="NUM_OF_ARRAY_ELEMS")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.array(prophy.u8, size=NUM_OF_ARRAY_ELEMS)),
    ]
"""
    assert serialize(nodes) == ref


def test_struct_rendering_with_limited_array():
    nodes = [model.Struct("Struct", [model.StructMember("a_len", "u8"),
                                     model.StructMember("a", "u8", bound="a_len", size="NUM_OF_ARRAY_ELEMS")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a_len', prophy.u8),
        ('a', prophy.array(prophy.u8, bound='a_len', size=NUM_OF_ARRAY_ELEMS)),
    ]
"""
    assert serialize(nodes) == ref


def test_struct_rendering_with_optional():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u32", optional=True)])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.optional(prophy.u32)),
    ]
"""
    assert serialize(nodes) == ref


def test_struct_rendering_with_byte():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte")])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.u8),
    ]
"""
    assert serialize(nodes) == ref


def test_struct_rendering_with_byte_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "byte", greedy=True)])]

    ref = """\
class Struct(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('a', prophy.bytes()),
    ]
"""
    assert serialize(nodes) == ref


def test_union_rendering():
    nodes = [model.Union("U", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "B", "1"),
                               model.UnionMember("c", "C", "2")])]

    ref = """\
class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
    _descriptor = [
        ('a', A, 0),
        ('b', B, 1),
        ('c', C, 2),
    ]
"""
    assert serialize(nodes) == ref


def test_union_rendering_2():
    nodes = [model.Union("U", [model.UnionMember("a", "i8", "0"),
                               model.UnionMember("b", "u32", "1"),
                               model.UnionMember("c", "r64", "2")])]

    ref = """\
class U(prophy.with_metaclass(prophy.union_generator, prophy.union)):
    _descriptor = [
        ('a', prophy.i8, 0),
        ('b', prophy.u32, 1),
        ('c', prophy.r64, 2),
    ]
"""
    assert serialize(nodes) == ref


def test_python_translator_1():
    ih = []
    th = []
    for x in range(20, 200, 60):
        ih.append(model.Include("test_include_" + str(x), [model.Constant("n_%s" % x, x, "doc")]))
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
# -*- encoding: utf-8 -*-
# This file has been generated by prophyc.

import prophy

from test_include_20 import n_20
from test_include_80 import n_80
from test_include_140 import n_140

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
        ('elem_91', val_91),
    ]


elem_1 = val_1
elem_31 = val_31
elem_61 = val_61
elem_91 = val_91


class MAC_L2CallConfigResp(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('messageResult', SMessageResult),
    ]
"""
    assert output == ref


def test_python_translator_2(larger_model):
    python_translator = _PythonTranslator()
    output = python_translator(larger_model, "")

    assert output == """\
# -*- encoding: utf-8 -*-
# This file has been generated by prophyc.

import prophy

from some_defs import IncludedStruct, c
from cplx import cint16_t, cint32_t

a = prophy.i16
c = a


class the_union(prophy.with_metaclass(prophy.union_generator, prophy.union)):
    _descriptor = [
        ('a', IncludedStruct, 0),
        ('field_with_a_long_name', cint16_t, 1),
        ('field_with_a_longer_name', cint32_t, 2),
        ('other', prophy.i32, 4090),
    ]


class E1(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators = [
        ('E1_A', 0),
        ('E1_B_has_a_long_name', 1),
        ('E1_C_desc', 2),
    ]


E1_A = 0
E1_B_has_a_long_name = 1
E1_C_desc = 2


class E2(prophy.with_metaclass(prophy.enum_generator, prophy.enum)):
    _enumerators = [
        ('E2_A', 0),
    ]


E2_A = 0
CONST_A = 6
CONST_B = 0


class StructMemberKinds(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
    _descriptor = [
        ('member_without_docstring', prophy.i16),
        ('ext_size', prophy.i16),
        ('optional_element', prophy.optional(cint16_t)),
        ('fixed_array', prophy.array(cint16_t, size=3)),
        ('samples', prophy.array(cint16_t, bound='ext_size')),
        ('limited_array', prophy.array(prophy.r64, bound='ext_size', size=4)),
        ('greedy', prophy.array(cint16_t)),
    ]
"""
