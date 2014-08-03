from prophyc import model
from prophyc import model_process
from util import *

def partition(nodes, name):
    pnodes = model_process.ProcessedNodes(nodes)
    members = pnodes.types[name].members
    return pnodes.partition(members)

def test_types():
    nodes = [model.Include("szydlo"),
             model.Constant("CONST_A", "0"),
             model.Typedef("a", "b")]

    pnodes = model_process.ProcessedNodes(nodes)

    assert pnodes.types == {
        "szydlo": model.Include("szydlo"),
        "CONST_A": model.Constant("CONST_A", "0"),
        "a": model.Typedef("a", "b")
    }

def test_kinds():
    nodes = [
        model.Struct("Empty", []),
        model.Struct("Dynamic", [
            make_member("a_len", "u8"),
            make_member("a", "u8", array = ("a_len", None))
        ]),
        model.Struct("Fixed", [
            make_member("a", "u8", array = (None, "10"))
        ]),
        model.Struct("Limited", [
            make_member("a_len", "u8"),
            make_member("a", "u8", array = ("a_len", "10"))
        ]),
        model.Struct("Greedy", [
            make_member("a", "byte", array = (None, None))
        ]),
        model.Struct("DynamicWrapper", [
            make_member("a", "Dynamic")
        ]),
        model.Struct("GreedyWrapper", [
            make_member("a", "Greedy")
        ]),
        model.Struct("GreedyDynamic", [
            make_member("a", "Dynamic", array = (None, None))
        ]),
        model.Typedef("TU8", "u8"),
        model.Typedef("TDynamic", "Dynamic"),
        model.Typedef("TGreedy", "Greedy"),
        model.Struct("TypedefedU8", [
            make_member("a", "TU8")
        ]),
        model.Struct("TypedefedDynamic", [
            make_member("a", "TDynamic")
        ]),
        model.Struct("TypedefedGreedy", [
            make_member("a", "TGreedy")
        ]),
        model.Typedef("TTDynamic", "TDynamic"),
        model.Typedef("TTTDynamic", "TTDynamic"),
        model.Struct("DeeplyTypedefed", [
            make_member("a", "TTTDynamic")
        ]),
    ]

    pnodes = model_process.ProcessedNodes(nodes)

    assert pnodes.kinds == {
        "Empty": model_process.StructKind.FIXED,
        "Dynamic": model_process.StructKind.DYNAMIC,
        "Fixed": model_process.StructKind.FIXED,
        "Limited": model_process.StructKind.FIXED,
        "Greedy": model_process.StructKind.UNLIMITED,
        "DynamicWrapper": model_process.StructKind.DYNAMIC,
        "GreedyWrapper": model_process.StructKind.UNLIMITED,
        "GreedyDynamic": model_process.StructKind.UNLIMITED,
        "TypedefedU8": model_process.StructKind.FIXED,
        "TypedefedDynamic": model_process.StructKind.DYNAMIC,
        "TypedefedGreedy": model_process.StructKind.UNLIMITED,
        "DeeplyTypedefed": model_process.StructKind.DYNAMIC,
    }

def test_partition_fixed():
    nodes = [
        model.Struct("Fixed", [
            make_member("a", "u8"),
            make_member("b", "u8"),
            make_member("c", "u8")
        ])
    ]

    main, parts = partition(nodes, "Fixed")

    assert main == [
        make_member("a", "u8"),
        make_member("b", "u8"),
        make_member("c", "u8")
    ]
    assert parts == []

def test_partition_many_arrays():
    nodes = [
        model.Struct("ManyArrays", [
            make_member("num_of_a", "u8"),
            make_member("a", "u8", array = ("num_of_a", None)),
            make_member("num_of_b", "u8"),
            make_member("b", "u8", array = ("num_of_b", None)),
            make_member("num_of_c", "u8"),
            make_member("c", "u8", array = ("num_of_c", None))
        ]),
    ]

    main, parts = partition(nodes, "ManyArrays")

    assert main == [
        make_member("num_of_a", "u8"),
        make_member("a", "u8", array = ("num_of_a", None))
    ]
    assert parts == [
        [
            make_member("num_of_b", "u8"),
            make_member("b", "u8", array = ("num_of_b", None))
        ],
        [
            make_member("num_of_c", "u8"),
            make_member("c", "u8", array = ("num_of_c", None))
        ]
    ]

def test_partition_many_arrays_mixed():
    nodes = [
        model.Struct("ManyArraysMixed", [
            make_member("num_of_a", "u8"),
            make_member("num_of_b", "u8"),
            make_member("a", "u8", array = ("num_of_a", None)),
            make_member("b", "u8", array = ("num_of_b", None))
        ]),
    ]

    main, parts = partition(nodes, "ManyArraysMixed")

    assert main == [
        make_member("num_of_a", "u8"),
        make_member("num_of_b", "u8"),
        make_member("a", "u8", array = ("num_of_a", None))
    ]
    assert parts == [
        [
            make_member("b", "u8", array = ("num_of_b", None))
        ]
    ]

def test_partition_dynamic_struct():
    nodes = [
        model.Struct("Dynamic", [
            make_member("num_of_a", "u8"),
            make_member("a", "u8", array = ("num_of_a", None))
        ]),
        model.Struct("X", [
            make_member("a", "u8"),
            make_member("b", "Dynamic"),
            make_member("c", "u8")
        ])
    ]

    main, parts = partition(nodes, "X")

    assert main == [
        make_member("a", "u8"),
        make_member("b", "Dynamic")
    ]
    assert parts == [
        [
            make_member("c", "u8")
        ]
    ]

def test_partition_many_dynamic_structs():
    nodes = [
        model.Struct("Dynamic", [
            make_member("num_of_a", "u8"),
            make_member("a", "u8", array = ("num_of_a", None))
        ]),
        model.Struct("X", [
            make_member("a", "Dynamic"),
            make_member("b", "Dynamic"),
            make_member("c", "Dynamic")
        ])
    ]

    main, parts = partition(nodes, "X")

    assert main == [
        make_member("a", "Dynamic")
    ]
    assert parts == [
        [
            make_member("b", "Dynamic")
        ],
        [
            make_member("c", "Dynamic")
        ]
    ]
