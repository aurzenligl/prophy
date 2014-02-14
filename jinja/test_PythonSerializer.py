import sys
import hashlib

import data_holder
import writer

linux_hashes = {
"test_of_PythonSerializer" : "5c2d6d350fdea2c825ed8e8fcd875f10",
"test_of_PythonSerializer_enum" : "26f524cefc1243e04e18bbee34eac884",
"test_of_PythonSerializer_import" : "da45c13ad54818957c1b932d8beb56f4"
}

windows_hashes = {
"test_of_PythonSerializer" : "af8c4ee390b6e906d2dfdf9336bf90c9",
"test_of_PythonSerializer_enum" : "275bf674a0c1025d10e929b39896213f",
"test_of_PythonSerializer_import" : "42b158e97a9e205de2178d6befaeed35"
}

hashes = linux_hashes if sys.platform == "linux2" else windows_hashes

def test_of_PythonSerializer():

    ih = data_holder.IncludeHolder()
    th = data_holder.TypeDefHolder()

    for x in range(20, 400, 60):
        ih.add_to_list("test_include_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "i_td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "u_td_elem_val_"+str(x))

    enum = data_holder.EnumHolder()
    for x in range(1, 200, 30):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))

    const = data_holder.ConstantHolder()
    const.add_to_list("C_A","5")
    const.add_to_list("C_B","5")
    const.add_to_list("C_C", "C_B + C_A")


    msg_h = data_holder.MessageHolder()
    msg_h.name = "MAC_L2CallConfigResp"
    msg_h.add_to_list(data_holder.MemberHolder('messageResult','SMessageResult'))


    dh = data_holder.DataHolder( include = ih, typedef = th , constant = const, msgs_list = [msg_h])
    dh.enum_dict["test"] = enum

    ps = writer.PythonSerializer()
    o =  ps.serialize(dh)
    assert hashes["test_of_PythonSerializer"] == hashlib.md5( o ).hexdigest()


def test_of_PythonSerializer_enum():
    ps = writer.PythonSerializer()
    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))
    o =  ps._serialize_enum( { "test" : enum } )
    assert hashes["test_of_PythonSerializer_enum"] ==  hashlib.md5(o).hexdigest()


def test_of_PythonSerializer_import():
    l = []
    for x in range(20, 400, 3):
        l.append("test_include_"+str(x))
    ps = writer.PythonSerializer()
    o = ps._serialize_include(l)
    assert hashes["test_of_PythonSerializer_import"] == hashlib.md5(o).hexdigest()
