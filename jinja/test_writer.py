import os
import writer
import data_holder

def test_of_WriterFabric_default_writer():
    assert type(writer.WriterFabric.get_writer("test.txt")) is writer.WriterTxt


def test_of_Python_Enum_Serializer():
    ps = writer.PythonSerializer();
    enum = data_holder.EnumHolder()
    for x in range(1, 200):
        enum.add_to_list("elem_" + str(x), "val_"+ str(x))
    dh = data_holder.DataHolder(None, enum, None);
    assert ("dupa" + os.linesep) ==  ps.serialize(dh)

