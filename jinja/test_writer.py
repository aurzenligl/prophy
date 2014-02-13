import writer

def test_of_WriterFabric_default_writer():
    assert type(writer.WriterFabric.get_writer("test.txt")) is writer.WriterTxt



