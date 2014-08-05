from prophyc import model

def test_struct_repr():
    struct = model.Struct("MyStruct", [
        model.StructMember("a", "u8"),
        model.StructMember("b", "u16", bound = 'xlen'),
        model.StructMember("c", "u32", size = 5),
        model.StructMember("d", "u64", bound = 'xlen', size = 5),
        model.StructMember("e", "UU", unlimited = True),
        model.StructMember("f", "UUUU", optional = True)
    ])
    assert str(struct) == """\
MyStruct
    u8 a
    u16 b<>(xlen)
    u32 c[5]
    u64 d<5>(xlen)
    UU e<...>
    UUUU* f
"""
