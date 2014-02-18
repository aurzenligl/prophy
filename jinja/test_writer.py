import writer

def test_of_WriterFabric_default_writer():
    assert type(writer.get_writer("test.py")) is writer.WriterTxt



