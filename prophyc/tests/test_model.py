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
        model.Typedef("D", "B")
    ]

    model.cross_reference(nodes)

    assert nodes[1].definition.name == "A"
    assert nodes[2].members[1].definition.definition.name == "A"
    assert nodes[3].definition.name == "B"
    assert nodes[3].definition.definition.name == "A"

def test_evaluate_kinds_arrays():
    nodes = [
        model.Struct("A", [
            model.StructMember("a", "u8"),
            model.StructMember("b", "u8", optional = True),
            model.StructMember("c", "u8", size = "5"),
            model.StructMember("d_len", "u8"),
            model.StructMember("d", "u8", bound = "d_len", size = "5"),
            model.StructMember("e_len", "u8"),
            model.StructMember("e", "u8", bound = "e_len"),
            model.StructMember("f", "u8", unlimited = True)
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)

    assert [x.kind for x in nodes[0].members] == [
        model.Kind.FIXED,
        model.Kind.FIXED,
        model.Kind.FIXED,
        model.Kind.FIXED,
        model.Kind.FIXED,
        model.Kind.FIXED,
        model.Kind.DYNAMIC,
        model.Kind.UNLIMITED,
    ]

def test_evaluate_kinds_struct_records():
    nodes = [
        model.Struct("Fix", [
            model.StructMember("a", "u8")
        ]),
        model.Struct("Dyn", [
            model.StructMember("a_len", "u8"),
            model.StructMember("a", "u8", bound = "a_len")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Dyn"),
            model.StructMember("b_len", "u8"),
            model.StructMember("b", "Fix", bound = "b_len"),
            model.StructMember("c", "Fix", unlimited = True)
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)

    assert [x.kind for x in nodes] == [
        model.Kind.FIXED,
        model.Kind.DYNAMIC,
        model.Kind.UNLIMITED,
    ]

    assert [x.kind for x in nodes[2].members] == [
        model.Kind.DYNAMIC,
        model.Kind.FIXED,
        model.Kind.DYNAMIC,
        model.Kind.UNLIMITED,
    ]

def test_evaluate_kinds_with_typedefs():
    nodes = [
        model.Struct("Empty", []),
        model.Struct("Dynamic", [
            model.StructMember("a_len", "u8"),
            model.StructMember("a", "u8", bound = "a_len")
        ]),
        model.Struct("Fixed", [
            model.StructMember("a", "u8", size = "10")
        ]),
        model.Struct("Limited", [
            model.StructMember("a_len", "u8"),
            model.StructMember("a", "u8", bound = "a_len", size = "10")
        ]),
        model.Struct("Greedy", [
            model.StructMember("a", "byte", unlimited = True)
        ]),
        model.Struct("DynamicWrapper", [
            model.StructMember("a", "Dynamic")
        ]),
        model.Struct("GreedyWrapper", [
            model.StructMember("a", "Greedy")
        ]),
        model.Struct("GreedyDynamic", [
            model.StructMember("a", "Dynamic", unlimited = True)
        ]),
        model.Typedef("TU8", "u8"),
        model.Typedef("TDynamic", "Dynamic"),
        model.Typedef("TGreedy", "Greedy"),
        model.Struct("TypedefedU8", [
            model.StructMember("a", "TU8")
        ]),
        model.Struct("TypedefedDynamic", [
            model.StructMember("a", "TDynamic")
        ]),
        model.Struct("TypedefedGreedy", [
            model.StructMember("a", "TGreedy")
        ]),
        model.Typedef("TTDynamic", "TDynamic"),
        model.Typedef("TTTDynamic", "TTDynamic"),
        model.Struct("DeeplyTypedefed", [
            model.StructMember("a", "TTTDynamic")
        ]),
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)

    assert [x.kind for x in nodes if isinstance(x, model.Struct)] == [
        model.Kind.FIXED,
        model.Kind.DYNAMIC,
        model.Kind.FIXED,
        model.Kind.FIXED,
        model.Kind.UNLIMITED,
        model.Kind.DYNAMIC,
        model.Kind.UNLIMITED,
        model.Kind.UNLIMITED,
        model.Kind.FIXED,
        model.Kind.DYNAMIC,
        model.Kind.UNLIMITED,
        model.Kind.DYNAMIC,
    ]
