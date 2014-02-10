import Reader

def test_read_a_file(setup_file_to_read):
    pass
    str_a = "W4VNrqXPfDt6eTMLitoWlX7i"
    file_entry = Reader.Reader.readFile(setup_file_to_read)
    assert str_a == file_entry
