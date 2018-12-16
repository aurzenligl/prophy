# -*- coding: utf-8 -*-
import sys

import pytest

from prophyc import model
from prophyc.model import Include, Constant, Typedef, Struct, StructMember, Union, UnionMember, Enum, EnumMember


def assert_repr_works(object_):
    """It works under assumption that __eq__ checks equality. """
    assert eval(repr(object_)) == object_


def test_typedef_str():
    typedef = Typedef("my_typedef", "u8")
    assert str(typedef) == "typedef u8 my_typedef;"


def test_typedef_repr():
    assert_repr_works(Typedef('my_typedef', 'u8', docstring='comment'))


def test_struct_repr():
    struct_a = Struct("MyStruct", [
        StructMember("a", "u8"),
        StructMember("b", "cint16_t"),
        StructMember("c", "u32", size=3, docstring="no_docstring"),
    ], docstring="no_docstring_")

    assert_repr_works(struct_a)
    assert repr(struct_a) == """\
Struct('MyStruct', [StructMember('a', 'u8', 'None', '', bound=None, size=None, unlimited=False, optional=False), \
StructMember('b', 'cint16_t', 'None', '', bound=None, size=None, unlimited=False, optional=False), \
StructMember('c', 'u32', 'None', 'no_docstring', bound=None, size=3, unlimited=False, optional=False)], \
'no_docstring_')"""


def test_struct_str():
    struct_with_arrays = Struct("MyStruct", [
        StructMember("sizer_field", "u8"),
        StructMember("b", "UserDefinedType"),
        StructMember("fixed_array", "u32", size=3, docstring="no_docstring"),
        StructMember("dynamic_array", "u32", bound='num_of_dynamic_array', has_implicit_mate=True),
        StructMember("limited_array", "r64", bound='num_of_limited_array', size=3, has_implicit_mate=True),
        StructMember("ext_sized_1", "i32", bound="sizer_field"),
        StructMember("ext_sized_2", "i16", bound="sizer_field"),
        StructMember("greedy_array", "u8", unlimited=True),
    ], docstring="no_docstring_")

    # todo: its against documentation
    assert str(struct_with_arrays) == """\
struct MyStruct {
    u8 sizer_field;
    UserDefinedType b;
    u32 fixed_array[3];
    u32 dynamic_array<>;
    r64 limited_array<3>;
    i32 ext_sized_1<@sizer_field>;
    i16 ext_sized_2<@sizer_field>;
    u8 greedy_array<...>;
};
"""


def test_union_repr():
    union = Union("MyUnion", [
        UnionMember("a", "u8", 1),
        UnionMember("b", "u16", 2),
        UnionMember("c", "u32", 3, docstring="deff")
    ])
    assert_repr_works(union)
    assert str(union) == """\
union MyUnion {
    1: u8 a;
    2: u16 b;
    3: u32 c;
};
"""


MODEL_NODE_SIZES = [
    (model.ModelNode, 72),
    (model.Constant, 72),
    (model.EnumMember, 72),
    (model.Include, 72),
    (model.Enum, 72),
    (model.Typedef, 80),
    (model.StructMember, 152),
    (model.Union, 96),
]

NODES_CTORS = [
    (model.Constant, ("ño", "value")),
    (model.EnumMember, ("ño", "value")),
    (model.Typedef, ("ño", "value")),
    (model.StructMember, ("ño", "value")),
    (model.UnionMember, ("ño", "tp_", 2)),
    (model.Include, ("ño", [])),
    (model.Struct, ("ño", [],)),
    (model.Union, ("ño", [])),
    (model.Enum, ("ño", [])),
]


@pytest.mark.parametrize("k, args", NODES_CTORS)
def test_unicode_handling(k, args):
    a = k(*args, docstring="used weird letter from 'jalapeño' word")
    b = k(*args, docstring="used weird letter from 'jalapeño' word")
    assert a == b
    assert a.doc_str == b.doc_str


@pytest.mark.parametrize("cls, expected_size", MODEL_NODE_SIZES)
def test_model_slots(cls, expected_size):
    if sys.version[0] == 2:
        assert sys.getsizeof(cls(1, 3)) == expected_size, "You missed slots in {} class".format(cls.__name__)


def test_model_slots_custom_ctor():
    if sys.version[0] == 2:
        assert sys.getsizeof(Struct("n", [])) == 96
        assert sys.getsizeof(UnionMember("n", 3, 2)) == 112


def test_split_after():
    generator = model.split_after([1, 42, 2, 3, 42, 42, 5], lambda x: x == 42)
    assert [x for x in generator] == [[1, 42], [2, 3, 42], [42], [5]]


def test_model_sort_enums():
    nodes = [Typedef("B", "A"),
             Typedef("C", "A"),
             Enum("A", [])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]


def test_model_sort_typedefs():
    nodes = [Typedef("A", "X"),
             Typedef("C", "B"),
             Typedef("B", "A"),
             Typedef("E", "D"),
             Typedef("D", "C")]

    model.topological_sort(nodes)

    assert ["A", "B", "C", "D", "E"] == [node.name for node in nodes]


def test_model_sort_structs():
    nodes = [Struct("C", [StructMember("a", "B"),
                          StructMember("b", "A"),
                          StructMember("c", "D")]),
             Struct("B", [StructMember("a", "X"),
                          StructMember("b", "A"),
                          StructMember("c", "Y")]),
             Struct("A", [StructMember("a", "X"),
                          StructMember("b", "Y"),
                          StructMember("c", "Z")])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]


def test_model_sort_struct_with_two_deps():
    nodes = [Struct("C", [StructMember("a", "B")]),
             Struct("B", [StructMember("a", "A")]),
             Struct("A", [StructMember("a", "X")])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]


def test_model_sort_struct_with_multiple_dependencies():
    nodes = [Struct("D", [StructMember("a", "A"),
                          StructMember("b", "B"),
                          StructMember("c", "C")]),
             Struct("C", [StructMember("a", "A"),
                          StructMember("b", "B")]),
             Struct("B", [StructMember("a", "A")]),
             Typedef("A", "TTypeX")]

    model.topological_sort(nodes)

    assert ["A", "B", "C", "D"] == [node.name for node in nodes]


def test_model_sort_union():
    nodes = [Typedef("C", "B"),
             Union("B", [UnionMember("a", "A", "0"),
                         UnionMember("b", "A", "1")]),
             Struct("A", [StructMember("a", "X")])]

    model.topological_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]


def test_model_sort_constants():
    nodes = [Constant("C_C", "C_A + C_B"),
             Constant("C_A", "1"),
             Constant("C_B", "2")]

    model.topological_sort(nodes)

    assert [("C_A", "1"), ("C_B", "2"), ("C_C", "C_A + C_B")] == nodes


def test_cross_reference_structs():
    nodes = [
        Struct("A", [
            StructMember("a", "u8")
        ]),
        Struct("B", [
            StructMember("a", "A"),
            StructMember("b", "u8")
        ]),
        Struct("C", [
            StructMember("a", "A"),
            StructMember("b", "B"),
            StructMember("c", "NON_EXISTENT")
        ]),
        Struct("D", [
            StructMember("a", "A"),
            StructMember("b", "B"),
            StructMember("c", "C")
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
        Struct("A", [
            StructMember("a", "u8")
        ]),
        Typedef("B", "A"),
        Struct("C", [
            StructMember("a", "A"),
            StructMember("b", "B")
        ]),
        Typedef("D", "B")
    ]

    model.cross_reference(nodes)

    assert nodes[1].definition.name == "A"
    assert nodes[2].members[1].definition.definition.name == "A"
    assert nodes[3].definition.name == "B"
    assert nodes[3].definition.definition.name == "A"


def test_cross_symbols_from_includes():
    nodes = [
        Include('x', [
            Include('y', [
                Typedef('ala', 'u32')
            ]),
            Struct('ola', [
                StructMember('a', 'ala'),
            ])
        ]),
        Struct('ula', [
            StructMember('a', 'ola'),
            StructMember('b', 'ala'),
        ])
    ]

    model.cross_reference(nodes)

    assert nodes[1].members[0].definition.name == 'ola'
    assert nodes[1].members[1].definition.name == 'ala'
    # cross-reference only needs to link definitions of first level of nodes
    assert nodes[0].members[1].members[0].definition is None


def test_cross_reference_array_size_from_includes():
    nodes = [
        Include('x', [
            Include('y', [
                Constant('NUM', '3'),
            ]),
            Enum('E', [
                EnumMember('E1', '1'),
                EnumMember('E3', 'NUM')
            ]),
        ]),
        Struct('X', [
            StructMember('x', 'u32', size='NUM'),
            StructMember('y', 'u32', size='E1'),
            StructMember('z', 'u32', size='UNKNOWN'),
            StructMember('a', 'u32', size='E3')
        ])
    ]

    model.cross_reference(nodes)

    assert nodes[1].members[0].numeric_size == 3
    assert nodes[1].members[1].numeric_size == 1
    assert nodes[1].members[2].numeric_size is None
    assert nodes[1].members[3].numeric_size == 3


def test_cross_reference_numeric_size_of_expression():
    nodes = [
        Constant('A', 12),
        Constant('B', 15),
        Constant('C', 'A*B'),
        Struct('X', [
            StructMember('x', 'u32', size='C'),
        ])
    ]

    model.cross_reference(nodes)

    assert nodes[3].members[0].numeric_size == 180


def test_cross_reference_expression_as_array_size():
    nodes = [
        Struct('X', [
            StructMember('x', 'u32', size='2 * 3'),
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
    nodes = [Typedef('X', 'Unknown')]
    warn = WarnFake()
    model.cross_reference(nodes, warn)
    assert warn.msgs == ["type 'Unknown' not found"]


def test_cross_reference_struct_warnings():
    nodes = [Struct('X', [StructMember('x', 'TypeUnknown', size='12 + NumUnknown')])]
    warn = WarnFake()
    model.cross_reference(nodes, warn)
    assert warn.msgs == ["type 'TypeUnknown' not found", "numeric constant 'NumUnknown' not found"]


def test_cross_reference_union_warnings():
    nodes = [Union('X', [UnionMember('x', 'TypeUnknown', '42')])]
    warn = WarnFake()
    model.cross_reference(nodes, warn)
    assert warn.msgs == ["type 'TypeUnknown' not found"]


def test_cross_reference_no_warning_about_primitive_types():
    warn = WarnFake()
    model.cross_reference([Typedef('X', 'u8')], warn)
    model.cross_reference([Typedef('X', 'u16')], warn)
    model.cross_reference([Typedef('X', 'u32')], warn)
    model.cross_reference([Typedef('X', 'u64')], warn)
    model.cross_reference([Typedef('X', 'i8')], warn)
    model.cross_reference([Typedef('X', 'i16')], warn)
    model.cross_reference([Typedef('X', 'i32')], warn)
    model.cross_reference([Typedef('X', 'i64')], warn)
    model.cross_reference([Typedef('X', 'r32')], warn)
    model.cross_reference([Typedef('X', 'r64')], warn)
    model.cross_reference([Typedef('X', 'byte')], warn)
    assert warn.msgs == []


def test_cross_reference_quadratic_complexity_include_performance_bug():
    """
    If type and numeric definitions from includes are processed each time,
    compilation times can skyrocket...
    """
    FACTOR = 10

    nodes = [Constant('X', 42), Typedef('Y', 'u8')] * FACTOR
    for i in range(FACTOR):
        nodes = [Include('inc%s' % i, nodes)] * FACTOR
    nodes.append(Struct('Z', [StructMember('x', 'u8', size='X')]))

    """This line will kill your cpu if cross-referencing algorithm is quadratic"""
    model.cross_reference(nodes)

    assert nodes[-1].members[0].numeric_size == 42


def test_evaluate_kinds_arrays():
    nodes = [
        Struct("A", [
            StructMember("a", "u8"),
            StructMember("b", "u8", optional=True),
            StructMember("c", "u8", size="5"),
            StructMember("d_len", "u8"),
            StructMember("d", "u8", bound="d_len", size="5"),
            StructMember("e_len", "u8"),
            StructMember("e", "u8", bound="e_len"),
            StructMember("f", "u8", unlimited=True)
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)

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
        Struct("Fix", [
            StructMember("a", "u8")
        ]),
        Struct("Dyn", [
            StructMember("a_len", "u8"),
            StructMember("a", "u8", bound="a_len")
        ]),
        Struct("X", [
            StructMember("a", "Dyn"),
            StructMember("b_len", "u8"),
            StructMember("b", "Fix", bound="b_len"),
            StructMember("c", "Fix", unlimited=True)
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)

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
        Struct("Empty", []),
        Struct("Dynamic", [
            StructMember("a_len", "u8"),
            StructMember("a", "u8", bound="a_len")
        ]),
        Struct("Fixed", [
            StructMember("a", "u8", size="10")
        ]),
        Struct("Limited", [
            StructMember("a_len", "u8"),
            StructMember("a", "u8", bound="a_len", size="10")
        ]),
        Struct("Greedy", [
            StructMember("a", "byte", unlimited=True)
        ]),
        Struct("DynamicWrapper", [
            StructMember("a", "Dynamic")
        ]),
        Struct("GreedyWrapper", [
            StructMember("a", "Greedy")
        ]),
        Struct("GreedyDynamic", [
            StructMember("a", "Dynamic", unlimited=True)
        ]),
        Typedef("TU8", "u8"),
        Typedef("TDynamic", "Dynamic"),
        Typedef("TGreedy", "Greedy"),
        Struct("TypedefedU8", [
            StructMember("a", "TU8")
        ]),
        Struct("TypedefedDynamic", [
            StructMember("a", "TDynamic")
        ]),
        Struct("TypedefedGreedy", [
            StructMember("a", "TGreedy")
        ]),
        Typedef("TTDynamic", "TDynamic"),
        Typedef("TTTDynamic", "TTDynamic"),
        Struct("DeeplyTypedefed", [
            StructMember("a", "TTTDynamic")
        ]),
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)

    assert [x.kind for x in nodes if isinstance(x, Struct)] == [
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
        Struct("Fixed", [
            StructMember("a", "u8"),
            StructMember("b", "u8"),
            StructMember("c", "u8")
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)
    main, parts = model.partition(nodes[0].members)

    assert [x.name for x in main] == ["a", "b", "c"]
    assert [[x.name for x in part] for part in parts] == []


def test_partition_many_arrays():
    nodes = [
        Struct("ManyArrays", [
            StructMember("num_of_a", "u8"),
            StructMember("a", "u8", bound="num_of_a"),
            StructMember("num_of_b", "u8"),
            StructMember("b", "u8", bound="num_of_b"),
            StructMember("num_of_c", "u8"),
            StructMember("c", "u8", bound="num_of_c")
        ]),
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)
    main, parts = model.partition(nodes[0].members)

    assert [x.name for x in main] == ["num_of_a", "a"]
    assert [[x.name for x in part] for part in parts] == [["num_of_b", "b"], ["num_of_c", "c"]]


def test_partition_many_arrays_mixed():
    nodes = [
        Struct("ManyArraysMixed", [
            StructMember("num_of_a", "u8"),
            StructMember("num_of_b", "u8"),
            StructMember("a", "u8", bound="num_of_a"),
            StructMember("b", "u8", bound="num_of_b")
        ]),
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)
    main, parts = model.partition(nodes[0].members)

    assert [x.name for x in main] == ["num_of_a", "num_of_b", "a"]
    assert [[x.name for x in part] for part in parts] == [["b"]]


def test_partition_dynamic_struct():
    nodes = [
        Struct("Dynamic", [
            StructMember("num_of_a", "u8"),
            StructMember("a", "u8", bound="num_of_a")
        ]),
        Struct("X", [
            StructMember("a", "u8"),
            StructMember("b", "Dynamic"),
            StructMember("c", "u8")
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)
    main, parts = model.partition(nodes[1].members)

    assert [x.name for x in main] == ["a", "b"]
    assert [[x.name for x in part] for part in parts] == [["c"]]


def test_partition_many_dynamic_structs():
    nodes = [
        Struct("Dynamic", [
            StructMember("num_of_a", "u8"),
            StructMember("a", "u8", bound="num_of_a")
        ]),
        Struct("X", [
            StructMember("a", "Dynamic"),
            StructMember("b", "Dynamic"),
            StructMember("c", "Dynamic")
        ])
    ]

    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)
    main, parts = model.partition(nodes[1].members)

    assert [x.name for x in main] == ["a"]
    assert [[x.name for x in part] for part in parts] == [["b"], ["c"]]


def process(nodes, warn=None):
    model.cross_reference(nodes)
    model.evaluate_stiffness_kinds(nodes)
    model.evaluate_sizes(nodes, **(warn and {'warn': warn} or {}))
    return nodes


def process_with_warnings(nodes):
    warnings = []
    process(nodes, lambda warning: warnings.append(warning))
    return nodes, warnings


def get_size_alignment_padding(node):
    return (
            isinstance(node, StructMember) and
            (node.byte_size, node.alignment, node.padding) or
            (node.byte_size, node.alignment)
    )


def get_members_and_node(node):
    return node.members + [node]


def test_evaluate_sizes_struct():
    nodes = process([
        Struct('X', [
            StructMember('x', 'u16'),
            StructMember('y', 'u8')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (2, 2, 0),
        (1, 1, 1),
        (4, 2)
    ]


def test_evaluate_sizes_nested_struct():
    nodes = process([
        Struct('U16', [
            StructMember('x', 'u16'),
        ]),
        Struct('X', [
            StructMember('x', 'u8'),
            StructMember('y', 'U16'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (1, 1, 1),
        (2, 2, 0),
        (4, 2)
    ]


def test_evaluate_sizes_fixed_array():
    nodes = process([
        Struct('X', [
            StructMember('x', 'u32'),
            StructMember('y', 'u8', size='3')
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 0),
        (3, 1, 1),
        (8, 4)
    ]


def test_evaluate_sizes_dynamic_array():
    nodes = process([
        Struct('X', [
            StructMember('num_of_x', 'u32'),
            StructMember('x', 'u8', bound='num_of_x'),
        ]),
        Struct('Y', [
            StructMember('x', 'u8'),
            StructMember('y', 'X'),
            StructMember('z', 'u8')
        ]),
        Struct('Z', [
            StructMember('x', 'X'),
            StructMember('y', 'u64')
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
        Struct('X', [
            StructMember('num_of_x', 'u32'),
            StructMember('x', 'u8', bound='num_of_x', size='2'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 0),
        (2, 1, 2),
        (8, 4)
    ]


def test_evaluate_sizes_greedy_array():
    nodes = process([
        Struct('X', [
            StructMember('num_of_x', 'u32'),
            StructMember('x', 'u8', unlimited=True),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 0),
        (0, 1, -4),
        (4, 4)
    ]


def test_evaluate_sizes_partial_padding():
    nodes = process([
        Struct('D', [
            StructMember('num_of_x', 'u32'),
            StructMember('x', 'u32', bound='num_of_x')
        ]),
        Struct('X', [
            StructMember('num_of_x', 'u32'),
            StructMember('x', 'u8', bound='num_of_x'),
            StructMember('y', 'u8'),
            StructMember('z', 'u64'),
        ]),
        Struct('Y', [
            StructMember('num_of_x', 'u32'),
            StructMember('x', 'u8', bound='num_of_x'),
            StructMember('num_of_y', 'u32'),
            StructMember('y', 'u64', bound='num_of_y'),
        ]),
        Struct('Z', [
            StructMember('d1', 'D'),
            StructMember('x', 'u8'),
            StructMember('d2', 'D'),
            StructMember('y1', 'u8'),
            StructMember('y2', 'u64'),
            StructMember('d3', 'D'),
            StructMember('z1', 'u8'),
            StructMember('z2', 'u8'),
            StructMember('z3', 'u16'),
        ]),
        Struct('ZZZ', [
            StructMember('num_of_x', 'u32'),
            StructMember('x', 'u16', bound='num_of_x'),
            StructMember('y', 'u16'),
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
        Typedef('T1', 'u32'),
        Struct('X', [
            StructMember('x', 'T1'),
        ]),
        Typedef('T2', 'T1'),
        Struct('Y', [
            StructMember('x', 'T2'),
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
        Enum('E', [
            EnumMember('E1', '1')
        ]),
        Struct('X', [
            StructMember('x', 'E'),
            StructMember('y', 'i8'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4, 0),
        (1, 1, 3),
        (8, 4)
    ]


def test_evaluate_sizes_floats():
    nodes = process([
        Struct('X', [
            StructMember('x', 'r32'),
            StructMember('y', 'r64'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (4, 4, 4),
        (8, 8, 0),
        (16, 8)
    ]


def test_evaluate_sizes_bytes():
    nodes = process([
        Struct('X', [
            StructMember('x', 'byte'),
            StructMember('y', 'byte', size=3),
            StructMember('num_of_z', 'u32'),
            StructMember('z', 'byte', bound='num_of_z')
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
        Struct('X', [
            StructMember('x', 'u32')
        ]),
        Struct('O1', [
            StructMember('x', 'u8', optional=True),
            StructMember('y', 'u16', optional=True),
            StructMember('z', 'u32', optional=True),
            StructMember('a', 'u64', optional=True)
        ]),
        Struct('O2', [
            StructMember('x', 'X', optional=True)
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
        Union('X', [
            UnionMember('x', 'u32', '1'),
            UnionMember('y', 'u32', '2'),
            UnionMember('z', 'u32', '3')
        ]),
        Union('Y', [
            UnionMember('x', 'u64', '1')
        ]),
        Union('Z', [
            UnionMember('x', 'X', '1'),
            UnionMember('y', 'Y', '2')
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
        Union('X', [
            UnionMember('x', 'u8', '1')
        ]),
        Union('Y', [
            UnionMember('x', 'u8', '1'),
            UnionMember('y', 'u64', '2')
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
        Struct('X', []),
        Union('X', []),
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[0]))) == [
        (0, 1)
    ]
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4)
    ]


def test_evaluate_sizes_unknown():
    nodes, warnings = process_with_warnings([
        Struct('X', [
            StructMember('x', 'u8'),
            StructMember('y', 'U'),
            StructMember('z', 'u32'),
        ]),
        Union('Y', [
            UnionMember('x', 'u32', '1'),
            UnionMember('y', 'U', '2'),
            UnionMember('z', 'u32', '3')
        ]),
        Typedef('U16', 'U'),
        Struct('Z', [
            StructMember('x', 'U16'),
            StructMember('y', 'Unknown'),
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
        Constant('NUM', '3'),
        Enum('E', [
            EnumMember('E1', '1'),
            EnumMember('E3', 'NUM')
        ]),
        Struct('X', [
            StructMember('x', 'u32', size='NUM'),
            StructMember('y', 'u32', size='E1'),
            StructMember('z', 'u32', size='E3')
        ]),
        Struct('Y', [
            StructMember('x', 'u32', size='UNKNOWN'),
            StructMember('y', 'u32')
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
        Include('input', [
            Enum('E', [
                EnumMember('E1', '1')
            ])
        ]),
        Struct('X', [
            StructMember('x', 'E'),
            StructMember('y', 'i8'),
        ])
    ])
    assert list(map(get_size_alignment_padding, get_members_and_node(nodes[1]))) == [
        (4, 4, 0),
        (1, 1, 3),
        (8, 4)
    ]


def test_enum_str_and_repr():
    E = Enum('TheEnum', [
        EnumMember('E1', 1),
        EnumMember('E2', '2'),
        EnumMember('E3', '3')
    ])
    assert str(E) == """\
enum TheEnum {
    E1 = 1;
    E2 = '2';
    E3 = '3';
};
"""
    assert_repr_works(E)


def test_wrong_struct_members_type_definition():
    expected_msg = "struct 'A' members must be a list, got str instead."
    with pytest.raises(model.ModelError, match=expected_msg):
        Struct("A", "string")


def test_wrong_struct_members_type_assignment():
    expected_msg = "struct 'A' members must be a list, got str instead."
    a = Struct("A", [])
    with pytest.raises(model.ModelError, match=expected_msg):
        a.members = "string"


def test_wrong_struct_member_type():
    expected_msg = "Each member of struct 'A' has to be a StructMember instance. Got str at index 1."
    with pytest.raises(model.ModelError, match=expected_msg):
        Struct("A", [
            StructMember('field_name', 'u32'),
            "string",
        ])
    expected_msg = "Each member of struct 'A' has to be a StructMember instance. Got UnionMember at index 0."
    with pytest.raises(model.ModelError, match=expected_msg):
        Struct("A", [
            UnionMember('field_name', 'u32', 2),
        ])


def test_wrong_union_member_type():
    expected_msg = "Each member of union 'U' has to be a UnionMember instance. Got str at index 1."
    with pytest.raises(model.ModelError, match=expected_msg):
        Union("U", [
            UnionMember('field_name', 'u32', 0),
            "string",
        ])

    expected_msg = "Each member of union 'U' has to be a UnionMember instance. Got StructMember at index 0."
    with pytest.raises(model.ModelError, match=expected_msg):
        Union("U", [
            StructMember('field_name', 'u32'),
        ])


def test_duplicated_identifiers_struct():
    with pytest.raises(model.ModelError, match="Duplicated 'field_name' identifier in struct A"):
        Struct("A", [
            StructMember('field_name', 'u32'),
            StructMember('field_name', 'u16'),
        ])


def test_duplicated_identifiers_union():
    with pytest.raises(model.ModelError, match="Duplicated 'field_name' identifier in union U"):
        Union("U", [
            UnionMember('field_name', 'u32', 0),
            UnionMember('field_name', 'u16', 1),
        ])
