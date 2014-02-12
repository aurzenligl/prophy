import os
import writer
import data_holder
import hashlib

def test_of_WriterFabric_default_writer():
    assert type(writer.WriterFabric.get_writer("test.txt")) is writer.WriterTxt


def test_of_Python_Enum_Serializer_enum():
    ps = writer.PythonSerializer()
    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))
    o =  ps._serialize_enum( { "test" : enum } ) 
    assert "26f524cefc1243e04e18bbee34eac884" ==  hashlib.md5(o).hexdigest()

def test_of_Python_Enum_Serializer_import():
    l = []
    for x in range(20, 400,3):
        l.append("test_include_"+str(x))
    ps = writer.PythonSerializer()
    o = ps._serialize_include(l)
    assert "42b158e97a9e205de2178d6befaeed35" == hashlib.md5(o).hexdigest()
