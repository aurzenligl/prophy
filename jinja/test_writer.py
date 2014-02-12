import os
import sys
import writer
import data_holder
import hashlib


linux_hashes = {
"test_of_PythonSerializer" : "11e1ffc3519be57eba208d6f740c7dd2",
"test_of_PythonSerializer_enum" : "e907ddf819d3a2558596ffb392eb626f",
"test_of_PythonSerializer_import" : "42b158e97a9e205de2178d6befaeed35"
}

windows_hashes = {
"test_of_PythonSerializer" : "1",
"test_of_PythonSerializer_enum" : "e",
"test_of_PythonSerializer_import" : "4"
}

hashes = linux_hashes if sys.platform == "linux2" else windows_hashes

def test_of_WriterFabric_default_writer():
    assert type(writer.WriterFabric.get_writer("test.txt")) is writer.WriterTxt


def test_of_PythonSerializer():
    ih = data_holder.IncludeHolder()
    th = data_holder.TypeDefHolder()

    for x in range(20, 40, 5):
        ih.add_to_list("test_include_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "i_td_elem_val_"+str(x))
        th.add_to_list("td_elem_name_"+str(x), "u_td_elem_val_"+str(x))

    enum = data_holder.EnumHolder()
    for x in range(1, 5):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))

    dh = data_holder.DataHolder( include = ih, typedef = th )
    dh.enum_dict["test_enum"] = enum


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
