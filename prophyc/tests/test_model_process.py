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
            model.StructMember("a", "u8"),
            model.StructMember("b", "u8"),
            model.StructMember("c", "u8")
        ])
    ]

    main, parts = partition(nodes, "Fixed")

    assert main == [
        model.StructMember("a", "u8"),
        model.StructMember("b", "u8"),
        model.StructMember("c", "u8")
    ]
    assert parts == []

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

    main, parts = partition(nodes, "ManyArrays")

    assert main == [
        model.StructMember("num_of_a", "u8"),
        model.StructMember("a", "u8", bound = "num_of_a")
    ]
    assert parts == [
        [
            model.StructMember("num_of_b", "u8"),
            model.StructMember("b", "u8", bound = "num_of_b")
        ],
        [
            model.StructMember("num_of_c", "u8"),
            model.StructMember("c", "u8", bound = "num_of_c")
        ]
    ]

def test_partition_many_arrays_mixed():
    nodes = [
        model.Struct("ManyArraysMixed", [
            model.StructMember("num_of_a", "u8"),
            model.StructMember("num_of_b", "u8"),
            model.StructMember("a", "u8", bound = "num_of_a"),
            model.StructMember("b", "u8", bound = "num_of_b")
        ]),
    ]

    main, parts = partition(nodes, "ManyArraysMixed")

    assert main == [
        model.StructMember("num_of_a", "u8"),
        model.StructMember("num_of_b", "u8"),
        model.StructMember("a", "u8", bound = "num_of_a")
    ]
    assert parts == [
        [
            model.StructMember("b", "u8", bound = "num_of_b")
        ]
    ]

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

    main, parts = partition(nodes, "X")

    assert main == [
        model.StructMember("a", "u8"),
        model.StructMember("b", "Dynamic")
    ]
    assert parts == [
        [
            model.StructMember("c", "u8")
        ]
    ]

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

    main, parts = partition(nodes, "X")

    assert main == [
        model.StructMember("a", "Dynamic")
    ]
    assert parts == [
        [
            model.StructMember("b", "Dynamic")
        ],
        [
            model.StructMember("c", "Dynamic")
        ]
    ]
