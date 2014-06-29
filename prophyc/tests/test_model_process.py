from prophyc import model
from prophyc import model_process

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
            model.StructMember("a_len", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "a_len", None, False)
        ]),
        model.Struct("Fixed", [
            model.StructMember("a", "u8", True, None, "10", False)
        ]),
        model.Struct("Limited", [
            model.StructMember("a_len", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "a_len", "10", False)
        ]),
        model.Struct("Greedy", [
            model.StructMember("a", "byte", True, None, None, None)
        ]),
        model.Struct("DynamicWrapper", [
            model.StructMember("a", "Dynamic", None, None, None, None)
        ]),
        model.Struct("GreedyWrapper", [
            model.StructMember("a", "Greedy", None, None, None, None)
        ]),
        model.Struct("GreedyDynamic", [
            model.StructMember("a", "Dynamic", True, None, None, None)
        ]),
        model.Typedef("TU8", "u8"),
        model.Typedef("TDynamic", "Dynamic"),
        model.Typedef("TGreedy", "Greedy"),
        model.Struct("TypedefedU8", [
            model.StructMember("a", "TU8", None, None, None, None)
        ]),
        model.Struct("TypedefedDynamic", [
            model.StructMember("a", "TDynamic", None, None, None, None)
        ]),
        model.Struct("TypedefedGreedy", [
            model.StructMember("a", "TGreedy", None, None, None, None)
        ]),
        model.Typedef("TTDynamic", "TDynamic"),
        model.Typedef("TTTDynamic", "TTDynamic"),
        model.Struct("DeeplyTypedefed", [
            model.StructMember("a", "TTTDynamic", None, None, None, None)
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
            model.StructMember("a", "u8", None, None, None, False),
            model.StructMember("b", "u8", None, None, None, False),
            model.StructMember("c", "u8", None, None, None, False)
        ])
    ]

    main, parts = partition(nodes, "Fixed")

    assert main == [
        model.StructMember("a", "u8", None, None, None, False),
        model.StructMember("b", "u8", None, None, None, False),
        model.StructMember("c", "u8", None, None, None, False)
    ]
    assert parts == []

def test_partition_many_arrays():
    nodes = [
        model.Struct("ManyArrays", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False),
            model.StructMember("num_of_b", "u8", None, None, None, False),
            model.StructMember("b", "u8", True, "num_of_b", None, False),
            model.StructMember("num_of_c", "u8", None, None, None, False),
            model.StructMember("c", "u8", True, "num_of_c", None, False)
        ]),
    ]

    main, parts = partition(nodes, "ManyArrays")

    assert main == [
        model.StructMember("num_of_a", "u8", None, None, None, False),
        model.StructMember("a", "u8", True, "num_of_a", None, False)
    ]
    assert parts == [
        [
            model.StructMember("num_of_b", "u8", None, None, None, False),
            model.StructMember("b", "u8", True, "num_of_b", None, False)
        ],
        [
            model.StructMember("num_of_c", "u8", None, None, None, False),
            model.StructMember("c", "u8", True, "num_of_c", None, False)
        ]
    ]

def test_partition_many_arrays_mixed():
    nodes = [
        model.Struct("ManyArraysMixed", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("num_of_b", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False),
            model.StructMember("b", "u8", True, "num_of_b", None, False)
        ]),
    ]

    main, parts = partition(nodes, "ManyArraysMixed")

    assert main == [
        model.StructMember("num_of_a", "u8", None, None, None, False),
        model.StructMember("num_of_b", "u8", None, None, None, False),
        model.StructMember("a", "u8", True, "num_of_a", None, False)
    ]
    assert parts == [
        [
            model.StructMember("b", "u8", True, "num_of_b", None, False)
        ]
    ]

def test_partition_dynamic_struct():
    nodes = [
        model.Struct("Dynamic", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False)
        ]),
        model.Struct("X", [
            model.StructMember("a", "u8", None, None, None, False),
            model.StructMember("b", "Dynamic", None, None, None, False),
            model.StructMember("c", "u8", None, None, None, False)
        ])
    ]

    main, parts = partition(nodes, "X")

    assert main == [
        model.StructMember("a", "u8", None, None, None, False),
        model.StructMember("b", "Dynamic", None, None, None, False)
    ]
    assert parts == [
        [
            model.StructMember("c", "u8", None, None, None, False)
        ]
    ]

def test_partition_many_dynamic_structs():
    nodes = [
        model.Struct("Dynamic", [
            model.StructMember("num_of_a", "u8", None, None, None, False),
            model.StructMember("a", "u8", True, "num_of_a", None, False)
        ]),
        model.Struct("X", [
            model.StructMember("a", "Dynamic", None, None, None, False),
            model.StructMember("b", "Dynamic", None, None, None, False),
            model.StructMember("c", "Dynamic", None, None, None, False)
        ])
    ]

    main, parts = partition(nodes, "X")

    assert main == [
        model.StructMember("a", "Dynamic", None, None, None, False)
    ]
    assert parts == [
        [
            model.StructMember("b", "Dynamic", None, None, None, False)
        ],
        [
            model.StructMember("c", "Dynamic", None, None, None, False)
        ]
    ]
