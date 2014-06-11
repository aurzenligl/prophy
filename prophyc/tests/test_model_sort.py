import model
import model_sort
from collections import namedtuple

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
    nodes = [model.Struct("C", [model.StructMember("a", "B", None, None, None, None),
                                model.StructMember("b", "A", None, None, None, None),
                                model.StructMember("c", "D", None, None, None, None)]),
             model.Struct("B", [model.StructMember("a", "X", None, None, None, None),
                                model.StructMember("b", "A", None, None, None, None),
                                model.StructMember("c", "Y", None, None, None, None)]),
             model.Struct("A", [model.StructMember("a", "X", None, None, None, None),
                                model.StructMember("b", "Y", None, None, None, None),
                                model.StructMember("c", "Z", None, None, None, None)])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_two_deps():
    nodes = [model.Struct("C", [model.StructMember("a", "B", None, None, None, None)]),
             model.Struct("B", [model.StructMember("a", "A", None, None, None, None)]),
             model.Struct("A", [model.StructMember("a", "X", None, None, None, None)])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_multiple_dependencies():
    nodes = [model.Struct("D", [model.StructMember("a", "A", None, None, None, None),
                                model.StructMember("b", "B", None, None, None, None),
                                model.StructMember("c", "C", None, None, None, None)]),
             model.Struct("C", [model.StructMember("a", "A", None, None, None, None),
                                model.StructMember("b", "B", None, None, None, None)]),
             model.Struct("B", [model.StructMember("a", "A", None, None, None, None)]),
             model.Typedef("A", "TTypeX")]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C", "D"] == [node.name for node in nodes]

def test_model_sort_union():
    nodes = [model.Typedef("C", "B"),
             model.Union("B", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "A", "1")]),
             model.Struct("A", [model.StructMember("a", "X", None, None, None, None)])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]