# -*- coding: utf-8 -*-

import model
import PythonSerializer

def serialize(holder):
    return PythonSerializer.PythonSerializer().serialize_string(holder, no_prolog = True)

def test_includes_rendering():
    holder = model.Model()
    holder.includes = ["szydlo", "mydlo", "powidlo"]

    ref = """\
from szydlo import *
from mydlo import *
from powidlo import *
"""
    assert ref == serialize(holder)

def test_typedefs_rendering():
    holder = model.Model()
    holder.typedefs = [("a", "b")]

    ref = """\
a = b
"""
    assert ref == serialize(holder)

def test_typedefs_rendering_with_changed_enum_order():
    holder = model.Model()
    holder.typedefs = [("TEnum2", "EEnum2")]
    holder.enums = [("EEnum1", [("EEnum1_1", "EEnum1_Val")]),
                    ("EEnum2", [("EEnum2_2", "EEnum2_Val")])]

    ref = """\
class EEnum2(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEnum2_2', EEnum2_Val)]

EEnum2_2 = EEnum2_Val

TEnum2 = EEnum2

class EEnum1(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEnum1_1', EEnum1_Val)]

EEnum1_1 = EEnum1_Val
"""
    assert ref == serialize(holder)

def test_typedefs_rendering_with_changed_struct_order():
    holder = model.Model()
    holder.typedefs = [("TStruct2", "SStruct2")]

    msg1 = model.Struct()
    msg1.name = "SStruct1"
    msg1.members.append(model.Struct.Member('x', 'u32', None, None, None))

    msg2 = model.Struct()
    msg2.name = "SStruct2"
    msg2.members.append(model.Struct.Member('y', 'i32', None, None, None))

    holder.structs = [msg1, msg2]

    ref = """\
class SStruct2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('y', prophy.i32)]

TStruct2 = SStruct2

class SStruct1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('x', prophy.u32)]
"""
    assert ref == serialize(holder)

def test_enums_rendering():
    holder = model.Model()
    holder.enums = [("EEnum", [("EEnum_A", "0"), ("EEnum_B", "1"), ("EEnum_C", "2")])]

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
    assert ref == serialize(holder)

def test_constants_rendering():
    holder = model.Model()
    holder.constants = [("CONST_A", "0"), ("CONST_B", "31")]

    ref = """\
CONST_A = 0
CONST_B = 31
"""
    assert ref == serialize(holder)

def test_struct_rendering():
    holder = model.Model()
    struct = model.Struct()
    struct.name = "Struct"
    struct.members.append(model.Struct.Member("a", "u8", None, None, None))
    struct.members.append(model.Struct.Member("b", "i64", None, None, None))
    struct.members.append(model.Struct.Member("c", "r32", None, None, None))
    struct.members.append(model.Struct.Member("d", "TTypeX", None, None, None))
    holder.structs = [struct]

    ref = """\
class Struct(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('a', prophy.u8),
                   ('b', prophy.i64),
                   ('c', prophy.r32),
                   ('d', TTypeX)]
"""
    assert ref == serialize(holder)

def test_struct_rendering_with_dynamic_array():
    holder = model.Model()
    struct = model.Struct()
    struct.name = "Struct"
    struct.members.append(model.Struct.Member("tmpName", "TNumberOfItems", None, None, None))
    struct.members.append(model.Struct.Member("a", "u8", True, "tmpName", None))
    holder.structs = [struct]

    ref = """\
class Struct(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('tmpName', TNumberOfItems),
                   ('a', prophy.array(u8, bound = 'tmpName'))]
"""
    assert ref == serialize(holder)

def test_struct_rendering_with_static_array():
    holder = model.Model()
    struct = model.Struct()
    struct.name = "Struct"
    struct.members.append(model.Struct.Member("a", "u8", True, None, "NUM_OF_ARRAY_ELEMS"))
    holder.structs = [struct]

    ref = """\
class Struct(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('a', prophy.array(u8, size = NUM_OF_ARRAY_ELEMS))]
"""
    assert ref == serialize(holder)

def test_of_PythonSerializer():
    ih = []
    th = []
    for x in range(20, 200, 60):
        ih.append("test_include_" + str(x))
        th.append(("td_elem_name_" + str(x), "td_elem_val_" + str(x)))
        th.append(("td_elem_name_" + str(x), "i_td_elem_val_" + str(x)))
        th.append(("td_elem_name_" + str(x), "u_td_elem_val_" + str(x)))

    enum = []
    for x in range(1, 100, 30):
        enum.append(("elem_" + str(x), "val_" + str(x)))

    msg_h = model.Struct()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.members.append(model.Struct.Member('messageResult', 'SMessageResult', None, None, None))

    dh = model.Model()
    dh.includes = ih
    dh.typedefs = th
    dh.constants = [("C_A", "5"), ("C_B", "5"), ("C_C", "C_B + C_A")]
    dh.structs = [msg_h]
    dh.enums = [("test", enum)]

    ps = PythonSerializer.PythonSerializer()
    output = ps.serialize_string(dh)

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
td_elem_name_20 = prophy.i_td_elem_val_20
td_elem_name_20 = prophy.u_td_elem_val_20
td_elem_name_80 = td_elem_val_80
td_elem_name_80 = prophy.i_td_elem_val_80
td_elem_name_80 = prophy.u_td_elem_val_80
td_elem_name_140 = td_elem_val_140
td_elem_name_140 = prophy.i_td_elem_val_140
td_elem_name_140 = prophy.u_td_elem_val_140

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
