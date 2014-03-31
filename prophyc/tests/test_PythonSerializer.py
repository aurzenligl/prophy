# -*- coding: utf-8 -*-

import model
import PythonSerializer

def serialize(nodes):
    return PythonSerializer.PythonSerializer().serialize_string(nodes, header = False)

def test_includes_rendering():
    nodes = [model.Include("szydlo"),
             model.Include("mydlo"),
             model.Include("powidlo")]

    ref = """\
from szydlo import *

from mydlo import *

from powidlo import *
"""
    assert ref == serialize(nodes)

def test_typedefs_rendering():
    nodes = [model.Typedef("a", "b")]

    ref = """\
a = b
"""
    assert ref == serialize(nodes)

def test_enums_rendering():
    nodes = [model.Enum("EEnum", [("EEnum_A", "0"),
                                  ("EEnum_B", "1"),
                                  ("EEnum_C", "2")])]

    ref = """\
class EEnum(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEnum_A', 0),
                     ('EEnum_B', 1),
                     ('EEnum_C', 2)]

EEnum_A = 0
EEnum_B = 1
EEnum_C = 2
"""
    assert ref == serialize(nodes)

def test_constants_rendering():
    nodes = [model.Constant("CONST_A", "0"),
             model.Constant("CONST_B", "31")]

    ref = """\
CONST_A = 0

CONST_B = 31
"""
    assert ref == serialize(nodes)

def test_struct_rendering():
    nodes = [model.Struct("Struct", [(model.StructMember("a", "u8", None, None, None)),
                                     (model.StructMember("b", "i64", None, None, None)),
                                     (model.StructMember("c", "r32", None, None, None)),
                                     (model.StructMember("d", "TTypeX", None, None, None))])]

    ref = """\
class Struct(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('a', prophy.u8),
                   ('b', prophy.i64),
                   ('c', prophy.r32),
                   ('d', TTypeX)]
"""
    assert ref == serialize(nodes)

def test_struct_rendering_with_dynamic_array():
    nodes = [model.Struct("Struct", [model.StructMember("tmpName", "TNumberOfItems", None, None, None),
                                     model.StructMember("a", "u8", True, "tmpName", None)])]

    ref = """\
class Struct(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName', TNumberOfItems),
                   ('a', prophy.array(prophy.u8, bound = 'tmpName'))]
"""
    assert ref == serialize(nodes)

def test_struct_rendering_with_static_array():
    nodes = [model.Struct("Struct", [model.StructMember("a", "u8", True, None, "NUM_OF_ARRAY_ELEMS")])]

    ref = """\
class Struct(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('a', prophy.array(prophy.u8, size = NUM_OF_ARRAY_ELEMS))]
"""
    assert ref == serialize(nodes)

def test_union_rendering():
    nodes = [model.Union("U", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "B", "1"),
                               model.UnionMember("c", "C", "2")])]

    ref = """\
class U(prophy.union):
    __metaclass__ = prophy.union_generator
    _descriptor = [('a', A, 0),
                   ('b', B, 1),
                   ('c', C, 2)]
"""
    assert ref == serialize(nodes)

def test_of_PythonSerializer():
    ih = []
    th = []
    for x in range(20, 200, 60):
        ih.append(model.Include("test_include_" + str(x)))
        th.append(model.Typedef("td_elem_name_" + str(x), "td_elem_val_" + str(x)))
        th.append(model.Typedef("td_elem_name_" + str(x), "i_td_elem_val_" + str(x)))
        th.append(model.Typedef("td_elem_name_" + str(x), "u_td_elem_val_" + str(x)))

    enum = []
    for x in range(1, 100, 30):
        enum.append(("elem_" + str(x), "val_" + str(x)))

    name = "MAC_L2CallConfigResp"
    members = [model.StructMember('messageResult', 'SMessageResult', None, None, None)]
    msg_h = model.Struct(name, members)

    nodes = []
    nodes += ih
    nodes += [model.Constant("C_A", "5"), model.Constant("C_B", "5"), model.Constant("C_C", "C_B + C_A")]
    nodes += th
    nodes += [model.Enum("test", enum)]
    nodes += [msg_h]

    ps = PythonSerializer.PythonSerializer()
    output = ps.serialize_string(nodes)

    ref = """\
import prophy

def bitMaskOr(x, y):
    return x | y

def shiftLeft(x, y):
    return x << y

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

class test(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('elem_1', val_1),
                     ('elem_31', val_31),
                     ('elem_61', val_61),
                     ('elem_91', val_91)]

elem_1 = val_1
elem_31 = val_31
elem_61 = val_61
elem_91 = val_91

class MAC_L2CallConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult', SMessageResult)]
"""
    assert ref == output
