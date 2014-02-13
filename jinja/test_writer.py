import os
import sys
import writer
import data_holder
import hashlib



linux_hashes = {
"test_of_PythonSerializer" : "dd20e4a505ee4625fd857f3962a4acf6",
"test_of_PythonSerializer_enum" : "ca82f0d3706c921db9ac4d37389a9c77",
"test_of_PythonSerializer_import" : "42b158e97a9e205de2178d6befaeed35"
}

windows_hashes = {
"test_of_PythonSerializer" : "bce7e420fbdb878941e28bf38c69b5fc",
"test_of_PythonSerializer_enum" : "9cbdcca5ebf27b8b8bcb2b7f080bcf6f",
"test_of_PythonSerializer_import" : "e57c2d6db6b44ecdabba127dd0532aa0"
}

hashes = linux_hashes if sys.platform == "linux2" else windows_hashes

def test_of_WriterFabric_default_writer():
    assert type(writer.WriterFabric.get_writer("test.txt")) is writer.WriterTxt


def test_of_PythonSerializer():

    ih = data_holder.IncludeHolder()
    th = data_holder.TypeDefHolder()

    for x in range(20, 400, 3):
        ih.add_to_list("test_include_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "i_td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "u_td_elem_val_"+str(x))

    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))

    dh = data_holder.DataHolder( include = ih, typedef = th )
    dh.enum_dict["test"] = enum


    ps = writer.PythonSerializer()
    o =  ps.serialize(dh)
    assert hashes["test_of_PythonSerializer"] == hashlib.md5( o ).hexdigest()

# def test_of_PythonSerializer_member():
#     msg=data_holder.MessageHolder()
#     member1=data_holder.MemberHolder()
#     member2=data_holder.MemberHolder()
#     member3=data_holder.MemberHolder()
#
#     msg.add_to_list(member1)
#     msg.add_to_list(member2)
#     msg.add_to_list(member3)
#     ps = writer.PythonSerializer()
#     o =  ps.serialize(dh)
#     assert hashes["test_of_PythonSerializer"] == hashlib.md5( o ).hexdigest()

def test_of_PythonSerializer_enum():
    ps = writer.PythonSerializer()
    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))
    o =  ps._serialize_enum( { "test" : enum } )
    assert hashes["test_of_PythonSerializer_enum"] ==  hashlib.md5(o).hexdigest()

def test_of_PythonSerializer_msg():
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
