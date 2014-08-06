from prophyc import model

def test_typedef_repr():
    typedef = model.Typedef("my_typedef", "u8")
    assert str(typedef) == "u8 my_typedef"

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


def test_cross_reference_structs():
    nodes = [
        model.Struct("A", [
            model.StructMember("a", "u8")
        ]),
        model.Struct("B", [
            model.StructMember("a", "A"),
            model.StructMember("b", "u8")
        ]),
        model.Struct("C", [
            model.StructMember("a", "A"),
            model.StructMember("b", "B"),
            model.StructMember("c", "NON_EXISTENT")
        ]),
        model.Struct("D", [
            model.StructMember("a", "A"),
            model.StructMember("b", "B"),
            model.StructMember("c", "C")
        ])
    ]

    model.cross_reference(nodes)

    definition_names = [[x.definition.name if x.definition else None for x in y.members] for y in nodes]
    assert definition_names == [
        [None],
        ['A', None],
        ['A', 'B', None],
        ['A', 'B', 'C']
    ]

def test_cross_reference_typedef():
    nodes = [
        model.Struct("A", [
            model.StructMember("a", "u8")
        ]),
        model.Typedef("B", "A"),
        model.Struct("C", [
            model.StructMember("a", "A"),
            model.StructMember("b", "B")
        ]),
        model.Typedef("D", "B"),
    ]

    model.cross_reference(nodes)

    assert nodes[1].definition.name == "A"
    assert nodes[2].members[1].definition.definition.name == "A"
    assert nodes[3].definition.name == "B"
    assert nodes[3].definition.definition.name == "A"
