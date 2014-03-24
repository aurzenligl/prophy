from prophyc import writer

def test_of_WriterFabric_default_writer(tmpdir_cwd):
    assert type(writer.get_writer("test.py")) is writer.WriterTxt
