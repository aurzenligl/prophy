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

def test_union_repr():
    union = model.Union("MyUnion", [
        model.UnionMember("a", "u8", 1),
        model.UnionMember("b", "u16", 2),
        model.UnionMember("c", "u32", 3)
    ])
    assert str(union.members[0]) == "1: u8 a"
    assert str(union.members[1]) == "2: u16 b"
    assert str(union.members[2]) == "3: u32 c"
    assert str(union) == """\
MyUnion
    1: u8 a
    2: u16 b
    3: u32 c
"""

def test_split_after():
    generator = model.split_after([1, 42, 2, 3, 42, 42, 5], lambda x: x == 42)
    assert [x for x in generator] == [[1, 42], [2, 3, 42], [42], [5]]

def test_model_sort_enums():
    nodes = [model.Typedef("B", "A"),
             model.Typedef("C", "A"),
             model.Enum("A", [])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_typedefs():
    nodes = [model.Typedef("A", "X"),
             model.Typedef("C", "B"),
             model.Typedef("B", "A"),
             model.Typedef("E", "D"),
             model.Typedef("D", "C")]

    model.topological_sort(nodes)

    assert ["A", "B", "C", "D", "E"] == [node.name for node in nodes]

def test_model_sort_structs():
    nodes = [model.Struct("C", [model.StructMember("a", "B"),
                                model.StructMember("b", "A"),
                                model.StructMember("c", "D")]),
             model.Struct("B", [model.StructMember("a", "X"),
                                model.StructMember("b", "A"),
                                model.StructMember("c", "Y")]),
             model.Struct("A", [model.StructMember("a", "X"),
                                model.StructMember("b", "Y"),
                                model.StructMember("c", "Z")])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_two_deps():
    nodes = [model.Struct("C", [model.StructMember("a", "B")]),
             model.Struct("B", [model.StructMember("a", "A")]),
             model.Struct("A", [model.StructMember("a", "X")])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_multiple_dependencies():
    nodes = [model.Struct("D", [model.StructMember("a", "A"),
                                model.StructMember("b", "B"),
                                model.StructMember("c", "C")]),
             model.Struct("C", [model.StructMember("a", "A"),
                                model.StructMember("b", "B")]),
             model.Struct("B", [model.StructMember("a", "A")]),
             model.Typedef("A", "TTypeX")]

    model.topological_sort(nodes)

    assert ["A", "B", "C", "D"] == [node.name for node in nodes]

def test_model_sort_union():
    nodes = [model.Typedef("C", "B"),
             model.Union("B", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "A", "1")]),
             model.Struct("A", [model.StructMember("a", "X")])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_constants():
    nodes = [model.Constant("C_C", "C_A + C_B"),
             model.Constant("C_A", "1"),
             model.Constant("C_B", "2")]

    model.topological_sort(nodes)

    assert [("C_A", "1"), ("C_B", "2"), ("C_C", "C_A + C_B")] == nodes

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

def test_cross_symbols_from_includes():
    nodes = [
        model.Include('x', [
            model.Include('y', [
                model.Typedef('ala', 'u32')
            ]),
            model.Struct('ola', [
                model.StructMember('a', 'ala'),
            ])
        ]),
        model.Struct('ula', [
            model.StructMember('a', 'ola'),
            model.StructMember('b', 'ala'),
        ])
    ]

    model.cross_reference(nodes)

    assert nodes[1].members[0].definition.name == 'ola'
    assert nodes[1].members[1].definition.name == 'ala'
    # cross-reference only needs to link definitions of first level of nodes
    assert nodes[0].nodes[1].members[0].definition is None

def test_cross_reference_array_size_from_includes():
    nodes = [
        model.Include('x', [
            model.Include('y', [
                model.Constant('NUM', '3'),
            ]),
            model.Enum('E', [
                model.EnumMember('E1', '1'),
                model.EnumMember('E3', 'NUM')
            ]),
        ]),
        model.Struct('X', [
            model.StructMember('x', 'u32', size = 'NUM'),
            model.StructMember('y', 'u32', size = 'E1'),
            model.StructMember('z', 'u32', size = 'UNKNOWN'),
            model.StructMember('a', 'u32', size = 'E3')
        ])
    ]

    model.cross_reference(nodes)

    assert nodes[1].members[0].numeric_size == 3
    assert nodes[1].members[1].numeric_size == 1
    assert nodes[1].members[2].numeric_size is None
    assert nodes[1].members[3].numeric_size == 3

def test_cross_reference_numeric_size_of_expression():
    nodes = [
        model.Constant('A', 12),
        model.Constant('B', 15),
        model.Constant('C', 'A*B'),
        model.Struct('X', [
            model.StructMember('x', 'u32', size = 'C'),
        ])
    ]

    model.cross_reference(nodes)

    assert nodes[3].members[0].numeric_size == 180

def test_cross_reference_expression_as_array_size():
    nodes = [
        model.Struct('X', [
            model.StructMember('x', 'u32', size = '2 * 3'),
        ])
    ]

    model.cross_reference(nodes)

    assert nodes[0].members[0].numeric_size == 6

class WarnFake(object):
    def __init__(self):
        self.msgs = []

    def __call__(self, msg):
        self.msgs.append(msg)

def test_cross_reference_typedef_warnings():
    nodes = [model.Typedef('X', 'Unknown')]
    warn = WarnFake()
    model.cross_reference(nodes, warn)
    assert warn.msgs == ["type 'Unknown' not found"]

def test_cross_reference_struct_warnings():
    nodes = [model.Struct('X', [model.StructMember('x', 'TypeUnknown', size = '12 + NumUnknown')])]
    warn = WarnFake()
    model.cross_reference(nodes, warn)
    assert warn.msgs == ["type 'TypeUnknown' not found", "numeric constant 'NumUnknown' not found"]

def test_cross_reference_union_warnings():
    nodes = [model.Union('X', [model.UnionMember('x', 'TypeUnknown', '42')])]
    warn = WarnFake()
    model.cross_reference(nodes, warn)
    assert warn.msgs == ["type 'TypeUnknown' not found"]

def test_cross_reference_no_warning_about_primitive_types():
    warn = WarnFake()
    model.cross_reference([model.Typedef('X', 'u8')], warn)
    model.cross_reference([model.Typedef('X', 'u16')], warn)
    model.cross_reference([model.Typedef('X', 'u32')], warn)
    model.cross_reference([model.Typedef('X', 'u64')], warn)
    model.cross_reference([model.Typedef('X', 'i8')], warn)
    model.cross_reference([model.Typedef('X', 'i16')], warn)
    model.cross_reference([model.Typedef('X', 'i32')], warn)
    model.cross_reference([model.Typedef('X', 'i64')], warn)
    model.cross_reference([model.Typedef('X', 'r32')], warn)
    model.cross_reference([model.Typedef('X', 'r64')], warn)
    model.cross_reference([model.Typedef('X', 'byte')], warn)
    assert warn.msgs == []

def test_cross_reference_quadratic_complexity_include_performance_bug():
    """
    If type and numeric definitions from includes are processed each time,
    compilation times can skyrocket...
    """
    FACTOR = 10

    nodes = [model.Constant('X', 42), model.Typedef('Y', 'u8')] * FACTOR
    for i in range(FACTOR):
        nodes = [model.Include('inc%s' % i, nodes)] * FACTOR
    nodes.append(model.Struct('Z', [model.StructMember('x', 'u8', size = 'X')]))

    """This line will kill your cpu if cross-referencing algorithm is quadratic"""
    model.cross_reference(nodes)

    assert nodes[-1].members[0].numeric_size == 42

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
        model.Kind.FIXED,
        model.Kind.FIXED,
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
        model.Kind.FIXED,
        model.Kind.FIXED,
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

def test_partition_fixed():
    nodes = [
        model.Struct("Fixed", [
            model.StructMember("a", "u8"),
            model.StructMember("b", "u8"),
            model.StructMember("c", "u8")
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    main, parts = model.partition(nodes[0].members)

    assert [x.name for x in main] == ["a", "b", "c"]
    assert [[x.name for x in part] for part in parts] == []

def test_partition_many_arrays():
    nodes = [
        model.Struct("ManyArrays", [
            model.StructMember("num_of_a", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a"),
            model.StructMember("num_of_b", "u8"),
            model.StructMember("b", "u8", bound = "num_of_b"),
            model.StructMember("num_of_c", "u8"),
            model.StructMember("c", "u8", bound = "num_of_c")
        ]),
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    main, parts = model.partition(nodes[0].members)

    assert [x.name for x in main] == ["num_of_a", "a"]
    assert [[x.name for x in part] for part in parts] == [["num_of_b", "b"], ["num_of_c", "c"]]

def test_partition_many_arrays_mixed():
    nodes = [
        model.Struct("ManyArraysMixed", [
            model.StructMember("num_of_a", "u8"),
            model.StructMember("num_of_b", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a"),
            model.StructMember("b", "u8", bound = "num_of_b")
        ]),
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    main, parts = model.partition(nodes[0].members)

    assert [x.name for x in main] == ["num_of_a", "num_of_b", "a"]
    assert [[x.name for x in part] for part in parts] == [["b"]]

def test_partition_dynamic_struct():
    nodes = [
        model.Struct("Dynamic", [
            model.StructMember("num_of_a", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a")
        ]),
        model.Struct("X", [
            model.StructMember("a", "u8"),
            model.StructMember("b", "Dynamic"),
            model.StructMember("c", "u8")
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    main, parts = model.partition(nodes[1].members)

    assert [x.name for x in main] == ["a", "b"]
    assert [[x.name for x in part] for part in parts] == [["c"]]

def test_partition_many_dynamic_structs():
    nodes = [
        model.Struct("Dynamic", [
            model.StructMember("num_of_a", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a")
        ]),
        model.Struct("X", [
            model.StructMember("a", "Dynamic"),
            model.StructMember("b", "Dynamic"),
            model.StructMember("c", "Dynamic")
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    main, parts = model.partition(nodes[1].members)

    assert [x.name for x in main] == ["a"]
    assert [[x.name for x in part] for part in parts] == [["b"], ["c"]]

def process(nodes, warn=None):
    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    model.evaluate_sizes(nodes, **(warn and {'warn': warn} or {}))
    return nodes

def process_with_warnings(nodes):
    warnings = []
    process(nodes, lambda warning: warnings.append(warning))
    return nodes, warnings

def get_size_alignment_padding(node):
    return (
        isinstance(node, model.StructMember) and
        (node.byte_size, node.alignment, node.padding) or
        (node.byte_size, node.alignment)
    )

def get_members_and_node(node):
    return node.members + [node]

def test_evaluate_sizes_struct():
    nodes = process([
        model.Struct('X', [
            model.StructMember('x', 'u16'),
            model.StructMember('y', 'u8')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (2, 2, 0),
        (1, 1, 1),
        (4, 2)
    ]

def test_evaluate_sizes_nested_struct():
    nodes = process([
        model.Struct('U16', [
            model.StructMember('x', 'u16'),
        ]),
        model.Struct('X', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'U16'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (1, 1, 1),
        (2, 2, 0),
        (4, 2)
    ]

def test_evaluate_sizes_fixed_array():
    nodes = process([
        model.Struct('X', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u8', size = '3')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 0),
        (3, 1, 1),
        (8, 4)
    ]

def test_evaluate_sizes_dynamic_array():
    nodes = process([
        model.Struct('X', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
        ]),
        model.Struct('Y', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'X'),
            model.StructMember('z', 'u8')
        ]),
        model.Struct('Z', [
            model.StructMember('x', 'X'),
            model.StructMember('y', 'u64')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 0),
        (0, 1, -4),
        (4, 4)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (1, 1, 3),
        (4, 4, 0),
        (1, 1, -4),
        (12, 4)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[2]))) == [
        (4, 4, -8),
        (8, 8, 0),
        (16, 8)
    ]

def test_evaluate_sizes_limited_array():
    nodes = process([
        model.Struct('X', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x', size = '2'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 0),
        (2, 1, 2),
        (8, 4)
    ]

def test_evaluate_sizes_greedy_array():
    nodes = process([
        model.Struct('X', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', unlimited = True),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 0),
        (0, 1, -4),
        (4, 4)
    ]

def test_evaluate_sizes_partial_padding():
    nodes = process([
        model.Struct('D', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u32', bound = 'num_of_x')
        ]),
        model.Struct('X', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
            model.StructMember('y', 'u8'),
            model.StructMember('z', 'u64'),
        ]),
        model.Struct('Y', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
            model.StructMember('num_of_y', 'u32'),
            model.StructMember('y', 'u64', bound = 'num_of_y'),
        ]),
        model.Struct('Z', [
            model.StructMember('d1', 'D'),
            model.StructMember('x', 'u8'),
            model.StructMember('d2', 'D'),
            model.StructMember('y1', 'u8'),
            model.StructMember('y2', 'u64'),
            model.StructMember('d3', 'D'),
            model.StructMember('z1', 'u8'),
            model.StructMember('z2', 'u8'),
            model.StructMember('z3', 'u16'),
        ]),
        model.Struct('ZZZ', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u16', bound = 'num_of_x'),
            model.StructMember('y', 'u16'),
        ]),
    ])

    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4, 0),
        (0, 1, -8),
        (1, 8, 7),
        (8, 8, 0),
        (24, 8)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[2]))) == [
        (4, 4, 0),
        (0, 1, -8),
        (4, 8, 4),
        (0, 8, 0),
        (16, 8)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[3]))) == [
        (4, 4, 0),
        (1, 4, 3),
        (4, 4, -8),
        (1, 8, 7),
        (8, 8, 0),
        (4, 4, 0),
        (1, 2, 0),
        (1, 1, 0),
        (2, 2, -8),
        (40, 8)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[4]))) == [
        (4, 4, 0),
        (0, 2, 0),
        (2, 2, -4),
        (8, 4)
    ]

def test_evaluate_sizes_typedef():
    nodes = process([
        model.Typedef('T1', 'u32'),
        model.Struct('X', [
            model.StructMember('x', 'T1'),
        ]),
        model.Typedef('T2', 'T1'),
        model.Struct('Y', [
            model.StructMember('x', 'T2'),
        ]),
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4, 0),
        (4, 4)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[3]))) == [
        (4, 4, 0),
        (4, 4)
    ]

def test_evaluate_sizes_enum():
    nodes = process([
        model.Enum('E', [
            model.EnumMember('E1', '1')
        ]),
        model.Struct('X', [
            model.StructMember('x', 'E'),
            model.StructMember('y', 'i8'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4, 0),
        (1, 1, 3),
        (8, 4)
    ]

def test_evaluate_sizes_floats():
    nodes = process([
        model.Struct('X', [
            model.StructMember('x', 'r32'),
            model.StructMember('y', 'r64'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 4),
        (8, 8, 0),
        (16, 8)
    ]

def test_evaluate_sizes_bytes():
    nodes = process([
        model.Struct('X', [
            model.StructMember('x', 'byte'),
            model.StructMember('y', 'byte', size = 3),
            model.StructMember('num_of_z', 'u32'),
            model.StructMember('z', 'byte', bound = 'num_of_z')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (1, 1, 0),
        (3, 1, 0),
        (4, 4, 0),
        (0, 1, -4),
        (8, 4)
    ]

def test_evaluate_sizes_optional():
    nodes = process([
        model.Struct('X', [
            model.StructMember('x', 'u32')
        ]),
        model.Struct('O1', [
            model.StructMember('x', 'u8', optional = True),
            model.StructMember('y', 'u16', optional = True),
            model.StructMember('z', 'u32', optional = True),
            model.StructMember('a', 'u64', optional = True)
        ]),
        model.Struct('O2', [
            model.StructMember('x', 'X', optional = True)
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (5, 4, 3),
        (6, 4, 2),
        (8, 4, 0),
        (16, 8, 0),
        (40, 8)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[2]))) == [
        (8, 4, 0),
        (8, 4)
    ]

def test_evaluate_sizes_union():
    nodes = process([
        model.Union('X', [
            model.UnionMember('x', 'u32', '1'),
            model.UnionMember('y', 'u32', '2'),
            model.UnionMember('z', 'u32', '3')
        ]),
        model.Union('Y', [
            model.UnionMember('x', 'u64', '1')
        ]),
        model.Union('Z', [
            model.UnionMember('x', 'X', '1'),
            model.UnionMember('y', 'Y', '2')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4),
        (4, 4),
        (4, 4),
        (8, 4)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (8, 8),
        (16, 8)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[2]))) == [
        (8, 4),
        (16, 8),
        (24, 8)
    ]

def test_evaluate_sizes_union_with_padding():
    nodes = process([
        model.Union('X', [
            model.UnionMember('x', 'u8', '1')
        ]),
        model.Union('Y', [
            model.UnionMember('x', 'u8', '1'),
            model.UnionMember('y', 'u64', '2')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (1, 1),
        (8, 4)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (1, 1),
        (8, 8),
        (16, 8)
    ]

def test_evaluate_sizes_empty():
    nodes = process([
        model.Struct('X', []),
        model.Union('X', []),
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (0, 1)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4)
    ]

def test_evaluate_sizes_unknown():
    nodes, warnings = process_with_warnings([
        model.Struct('X', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'U'),
            model.StructMember('z', 'u32'),
        ]),
        model.Union('Y', [
            model.UnionMember('x', 'u32', '1'),
            model.UnionMember('y', 'U', '2'),
            model.UnionMember('z', 'u32', '3')
        ]),
        model.Typedef('U16', 'U'),
        model.Struct('Z', [
            model.StructMember('x', 'U16'),
            model.StructMember('y', 'Unknown'),
        ]),
    ])

    assert warnings == [
        'X::y has unknown type "U"',
        'Y::y has unknown type "U"',
        'Z::x has unknown type "U"',
        'Z::y has unknown type "Unknown"'
    ]

    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (1, 1, None),
        (None, None, None),
        (4, 4, None),
        (None, None)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4),
        (None, None),
        (4, 4),
        (None, None)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[3]))) == [
        (None, None, None),
        (None, None, None),
        (None, None)
    ]

def test_evaluate_sizes_array_with_named_size():
    nodes = process([
        model.Constant('NUM', '3'),
        model.Enum('E', [
            model.EnumMember('E1', '1'),
            model.EnumMember('E3', 'NUM')
        ]),
        model.Struct('X', [
            model.StructMember('x', 'u32', size = 'NUM'),
            model.StructMember('y', 'u32', size = 'E1'),
            model.StructMember('z', 'u32', size = 'E3')
        ]),
        model.Struct('Y', [
            model.StructMember('x', 'u32', size = 'UNKNOWN'),
            model.StructMember('y', 'u32')
        ])

    ])

    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[2]))) == [
        (12, 4, 0),
        (4, 4, 0),
        (12, 4, 0),
        (28, 4)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[3]))) == [
        (None, None, None),
        (4, 4, None),
        (None, None)
    ]

def test_evaluate_sizes_with_include():
    nodes = process([
        model.Include('input', [
            model.Enum('E', [
                model.EnumMember('E1', '1')
            ])
        ]),
        model.Struct('X', [
            model.StructMember('x', 'E'),
            model.StructMember('y', 'i8'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4, 0),
        (1, 1, 3),
        (8, 4)
    ]

def test_enum_repr():
    E = model.Enum('TheEnum', [
        model.EnumMember('E1', '1'),
        model.EnumMember('E2', '2'),
        model.EnumMember('E3', '3')
    ])
    assert repr(E) == """\
TheEnum
    E1 1
    E2 2
    E3 3
"""
