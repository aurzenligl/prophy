import os
import writer
import data_holder
import hashlib

def test_of_WriterFabric_default_writer():
    assert type(writer.WriterFabric.get_writer("test.txt")) is writer.WriterTxt


def test_of_PythonSerializer():

    ih = data_holder.IncludeHolder()
    for x in range(20, 400, 3):
        ih.add_to_list("test_include_"+str(x))


    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))

    dh = data_holder.DataHolder()
    dh.enum_dict["test"] = enum

    ps = writer.PythonSerializer()
    assert "f2ae92ff2ad5e850aaa6077d0d63956b" == hashlib.md5( ps.serialize(dh) ).hexdigest()

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
