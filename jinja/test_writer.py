import os
import writer
import data_holder
import hashlib

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
    assert "dd20e4a505ee4625fd857f3962a4acf6" == hashlib.md5( o ).hexdigest()

def test_of_PythonSerializer_enum():
    ps = writer.PythonSerializer()
    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))
    o =  ps._serialize_enum( { "test" : enum } )
    assert "ca82f0d3706c921db9ac4d37389a9c77" ==  hashlib.md5(o).hexdigest()

def test_of_PythonSerializer_import():
    l = []
    for x in range(20, 400, 3):
        l.append("test_include_"+str(x))
    ps = writer.PythonSerializer()
    o = ps._serialize_include(l)
    assert "42b158e97a9e205de2178d6befaeed35" == hashlib.md5(o).hexdigest()
