from prophyc import model
from prophyc import model_sort

def test_model_sort_enums():
    nodes = [model.Typedef("B", "A"),
             model.Typedef("C", "A"),
             model.Enum("A", [])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_typedefs():
    nodes = [model.Typedef("A", "X"),
             model.Typedef("C", "B"),
             model.Typedef("B", "A"),
             model.Typedef("E", "D"),
             model.Typedef("D", "C")]

    model_sort.model_sort(nodes)

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

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_two_deps():
    nodes = [model.Struct("C", [model.StructMember("a", "B")]),
             model.Struct("B", [model.StructMember("a", "A")]),
             model.Struct("A", [model.StructMember("a", "X")])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_multiple_dependencies():
    nodes = [model.Struct("D", [model.StructMember("a", "A"),
                                model.StructMember("b", "B"),
                                model.StructMember("c", "C")]),
             model.Struct("C", [model.StructMember("a", "A"),
                                model.StructMember("b", "B")]),
             model.Struct("B", [model.StructMember("a", "A")]),
             model.Typedef("A", "TTypeX")]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C", "D"] == [node.name for node in nodes]

def test_model_sort_union():
    nodes = [model.Typedef("C", "B"),
             model.Union("B", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "A", "1")]),
             model.Struct("A", [model.StructMember("a", "X")])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_constants():
    nodes = [model.Constant("C_C", "C_A + C_B"),
             model.Constant("C_A", "1"),
             model.Constant("C_B", "2")]

    model_sort.model_sort(nodes)

    assert [("C_A", "1"), ("C_B", "2"), ("C_C", "C_A + C_B")] == nodes
