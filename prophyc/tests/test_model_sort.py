from prophyc import model
from prophyc import model_sort
from util import *

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
    nodes = [model.Struct("C", [make_member("a", "B"),
                                make_member("b", "A"),
                                make_member("c", "D")]),
             model.Struct("B", [make_member("a", "X"),
                                make_member("b", "A"),
                                make_member("c", "Y")]),
             model.Struct("A", [make_member("a", "X"),
                                make_member("b", "Y"),
                                make_member("c", "Z")])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_two_deps():
    nodes = [model.Struct("C", [make_member("a", "B")]),
             model.Struct("B", [make_member("a", "A")]),
             model.Struct("A", [make_member("a", "X")])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_struct_with_multiple_dependencies():
    nodes = [model.Struct("D", [make_member("a", "A"),
                                make_member("b", "B"),
                                make_member("c", "C")]),
             model.Struct("C", [make_member("a", "A"),
                                make_member("b", "B")]),
             model.Struct("B", [make_member("a", "A")]),
             model.Typedef("A", "TTypeX")]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C", "D"] == [node.name for node in nodes]

def test_model_sort_union():
    nodes = [model.Typedef("C", "B"),
             model.Union("B", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "A", "1")]),
             model.Struct("A", [make_member("a", "X")])]

    model_sort.model_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_model_sort_constants():
    nodes = [model.Constant("C_C", "C_A + C_B"),
             model.Constant("C_A", "1"),
             model.Constant("C_B", "2")]

    model_sort.model_sort(nodes)

    assert [("C_A", "1"), ("C_B", "2"), ("C_C", "C_A + C_B")] == nodes
