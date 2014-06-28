from prophyc import model
from prophyc import model_process

def test_types():
    nodes = [model.Include("szydlo"),
             model.Constant("CONST_A", "0"),
             model.Typedef("a", "b")]

    types = model_process.build_types(nodes)

    assert types == {
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

    types = model_process.build_types(nodes)
    kinds = model_process.build_kinds(types, nodes)

    assert kinds == {
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
