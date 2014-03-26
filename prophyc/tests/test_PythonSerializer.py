# -*- coding: utf-8 -*-

import DataHolder
import PythonSerializer

""" FIXME kl. this test is way too large. It needs to be split to multiple tests """
def test_of_PythonSerializer():
    ih = DataHolder.IncludeHolder()
    th = DataHolder.TypeDefHolder()
    for x in range(20, 200, 60):
        ih.add_to_list("test_include_" + str(x))
        th.add_to_list("td_elem_name_" + str(x), "td_elem_val_" + str(x))
        th.add_to_list("td_elem_name_" + str(x), "i_td_elem_val_" + str(x))
        th.add_to_list("td_elem_name_" + str(x), "u_td_elem_val_" + str(x))

    enum = DataHolder.EnumHolder()
    for x in range(1, 100, 30):
        enum.add_to_list("elem_" + str(x), "val_" + str(x))

    const = DataHolder.ConstantHolder()
    const.add_to_list("C_A", "5")
    const.add_to_list("C_B", "5")
    const.add_to_list("C_C", "C_B + C_A")

    msg_h = DataHolder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(DataHolder.MemberHolder('messageResult', 'SMessageResult'))

    dh = DataHolder.DataHolder(include = ih, typedef = th, constant = const, msgs_list = [msg_h])
    dh.enum_dict["test"] = enum

    ps = PythonSerializer.PythonSerializer()
    output = ps.serialize_to_string(dh)

    assert output == ("import prophy \n"
                      "from test_include_20 import *\n"
                      "from test_include_80 import *\n"
                      "from test_include_140 import *\n"
                      "\n"
                      "\n"
                      "C_B = 5\n"
                      "C_A = 5\n"
                      "C_C = C_B + C_A\n"
                      "\n"
                      "td_elem_name_20 = td_elem_val_20\n"
                      "td_elem_name_20 = prophy.i_td_elem_val_20\n"
                      "td_elem_name_20 = prophy.u_td_elem_val_20\n"
                      "td_elem_name_80 = td_elem_val_80\n"
                      "td_elem_name_80 = prophy.i_td_elem_val_80\n"
                      "td_elem_name_80 = prophy.u_td_elem_val_80\n"
                      "td_elem_name_140 = td_elem_val_140\n"
                      "td_elem_name_140 = prophy.i_td_elem_val_140\n"
                      "td_elem_name_140 = prophy.u_td_elem_val_140\n"
                      "\n"
                      "class test(prophy.enum):\n"
                      "    __metaclass__ = prophy.enum_generator\n"
                      "    _enumerators  = [('elem_1',val_1), ('elem_31',val_31), ('elem_61',val_61), ('elem_91',val_91)]\n"
                      "\n"
                      "class MAC_L2CallConfigResp(prophy.struct):\n"
                      "    __metaclass__ = prophy.struct_generator\n"
                      "    _descriptor = [('messageResult',SMessageResult)]\n")

def test_of_PythonSerializer_enum():
    enum = DataHolder.EnumHolder()
    for x in range(1, 5):
        enum.add_to_list("elem_" + str(x), "val_" + str(x))

    ps = PythonSerializer.PythonSerializer()
    output = ps._serialize_enum({ "test" : enum })

    """ FIXME kl. it's better to list enumerators and fields from newlines, to make output human-readable """
    assert output == ("class test(prophy.enum):\n"
                      "    __metaclass__ = prophy.enum_generator\n"
                      "    _enumerators  = [('elem_1',val_1), ('elem_2',val_2), ('elem_3',val_3), ('elem_4',val_4)]\n")

def test_of_PythonSerializer_import():
    includes = ["test_include_" + str(x) for x in xrange(0, 15, 3)]

    ps = PythonSerializer.PythonSerializer()
    output = ps._serialize_include(includes)

    """ FIXME kl. there seems to be a surplus space character at the end of "import prophy" line"""
    assert output == ('import prophy \n'
                      'from test_include_0 import *\n'
                      'from test_include_3 import *\n'
                      'from test_include_6 import *\n'
                      'from test_include_9 import *\n'
                      'from test_include_12 import *\n')
