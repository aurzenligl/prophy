# -*- coding: utf-8 -*-

import DataHolder
import PythonSerializer

def serialize(holder):
    return PythonSerializer.PythonSerializer().serialize_string(holder)

def test_includes_rendering():
    holder = DataHolder.DataHolder()
    holder.includes = ["szydlo", "mydlo", "powidlo"]

    ref = """\
import prophy

from szydlo import *
from mydlo import *
from powidlo import *
"""
    assert ref == serialize(holder)

def test_typedefs_rendering():
    holder = DataHolder.DataHolder()
    holder.typedefs = [("a", "b")]

    ref = """\
import prophy

a = b
"""
    assert ref == serialize(holder)

def test_typedefs_rendering_with_changed_enum_order():
    holder = DataHolder.DataHolder()
    holder.typedefs = [("TEnum2", "EEnum2")]
    holder.enum_dict["EEnum1"] = [("EEnum1_1", "EEnum1_Val")]
    holder.enum_dict["EEnum2"] = [("EEnum2_2", "EEnum2_Val")]

    ref = """\
import prophy

class EEnum2(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEnum2_2',EEnum2_Val)]

EEnum2_2 = EEnum2_Val

TEnum2 = EEnum2

class EEnum1(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEnum1_1',EEnum1_Val)]

EEnum1_1 = EEnum1_Val
"""
    assert ref == serialize(holder)

def test_typedefs_rendering_with_changed_struct_order():
    holder = DataHolder.DataHolder()
    holder.typedefs = [("TStruct2", "SStruct2")]

    msg1 = DataHolder.MessageHolder()
    msg1.name = "SStruct1"
    msg1.add_to_list(DataHolder.MemberHolder('x', 'u32'))

    msg2 = DataHolder.MessageHolder()
    msg2.name = "SStruct2"
    msg2.add_to_list(DataHolder.MemberHolder('y', 'i32'))

    holder.struct_list = [msg1, msg2]

    ref = """\
import prophy

class SStruct2(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('y',prophy.i32)]

TStruct2 = SStruct2

class SStruct1(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('x',prophy.u32)]
"""
    assert ref == serialize(holder)

def test_enums_rendering():
    holder = DataHolder.DataHolder()
    holder.enum_dict = {"EEnum": [("EEnum_A", "0"), ("EEnum_B", "1"), ("EEnum_C", "2")]}

    ref = """\
import prophy

class EEnum(prophy.enum):
    __metaclass__ = prophy.enum_generator
    _enumerators  = [('EEnum_A',0),
                     ('EEnum_B',1),
                     ('EEnum_C',2)]

EEnum_A = 0
EEnum_B = 1
EEnum_C = 2
"""
    assert ref == serialize(holder)

""" FIXME kl. this test is way too large. It needs to be split to multiple tests """
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

    const = DataHolder.ConstantHolder()
    const.add_to_list("C_A", "5")
    const.add_to_list("C_B", "5")
    const.add_to_list("C_C", "C_B + C_A")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(DataHolder.MemberHolder('messageResult', 'SMessageResult'))

    dh = DataHolder.DataHolder()
    dh.includes = ih
    dh.typedefs = th
    dh.constant = const
    dh.msgs_list = [msg_h]
    dh.enum_dict["test"] = enum

    ps = PythonSerializer.PythonSerializer()
    output = ps.serialize_string(dh)

    ref = """\
import prophy

from test_include_20 import *
from test_include_80 import *
from test_include_140 import *

C_B = 5
C_A = 5
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
    _enumerators  = [('elem_1',val_1),
                     ('elem_31',val_31),
                     ('elem_61',val_61),
                     ('elem_91',val_91)]

elem_1 = val_1
elem_31 = val_31
elem_61 = val_61
elem_91 = val_91

class MAC_L2CallConfigResp(prophy.struct):
    __metaclass__ = prophy.struct_generator
    _descriptor = [('messageResult',SMessageResult)]
"""
    assert ref == output
