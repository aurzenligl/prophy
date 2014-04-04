# -*- coding: utf-8 -*-

import model
import IsarParser
import PythonSerializer
from collections import namedtuple

def parse(xml_string):
    return IsarParser.IsarParser().parse_string(xml_string)

def test_includes_parsing():
    xml = """\
<system xmlns:xi="http://www.nsn.com/2008/XInclude">
    <xi:include href="mydlo.xml"/>
    <xi:include href="szydlo.xml"/>
    <xi:include href="powidlo.xml"/>
</system>
"""
    nodes = parse(xml)

    assert [("mydlo",), ("szydlo",), ("powidlo",)] == nodes

def test_constants_parsing():
    xml = """\
<x>
    <constant name="CONST_A" value="0"/>
    <constant name="CONST_B" value="31"/>
</x>
"""
    nodes = parse(xml)

    assert [("CONST_A", "0"), ("CONST_B", "31")] == nodes

def test_constants_parsing_and_sorting():
    xml = """\
<x>
    <constant name="C_C" value="C_A + C_B"/>
    <constant name="C_A" value="1"/>
    <constant name="C_B" value="2"/>
</x>
"""
    nodes = parse(xml)

    assert [("C_A", "1"), ("C_B", "2"), ("C_C", "C_A + C_B")] == nodes

def test_typedefs_primitive_type_parsing():
    xml = """\
<x>
    <typedef name="a" primitiveType="8 bit integer unsigned"/>
    <typedef name="b" primitiveType="16 bit integer unsigned"/>
    <typedef name="c" primitiveType="32 bit integer unsigned"/>
    <typedef name="d" primitiveType="64 bit integer unsigned"/>
    <typedef name="e" primitiveType="8 bit integer signed"/>
    <typedef name="f" primitiveType="16 bit integer signed"/>
    <typedef name="g" primitiveType="32 bit integer signed"/>
    <typedef name="h" primitiveType="64 bit integer signed"/>
    <typedef name="i" primitiveType="32 bit float"/>
    <typedef name="j" primitiveType="64 bit float"/>
</x>
"""
    nodes = parse(xml)

    assert [("a", "u8"),
            ("b", "u16"),
            ("c", "u32"),
            ("d", "u64"),
            ("e", "i8"),
            ("f", "i16"),
            ("g", "i32"),
            ("h", "i64"),
            ("i", "r32"),
            ("j", "r64")] == nodes

def test_typedefs_parsing():
    xml = """\
<x>
    <typedef name="TILoveTypedefs_ALot" type="MyType"/>
</x>
"""
    nodes = parse(xml)

    assert [("TILoveTypedefs_ALot", "MyType")] == nodes

def test_enums_parsing():
    xml = """\
<x>
    <enum name="EEnum">
        <enum-member name="EEnum_A" value="0"/>
        <enum-member name="EEnum_B" value="1"/>
        <enum-member name="EEnum_C" value="-1"/>
    </enum>
</x>
"""
    nodes = parse(xml)

    assert 1 == len(nodes)
    assert "EEnum" == nodes[0][0]
    assert [("EEnum_A", "0"), ("EEnum_B", "1"), (u"EEnum_C", "0xFFFFFFFF")] == nodes[0][1]

def test_struct_parsing():
    xml = """\
<x>
    <struct name="Struct">
        <member name="a" type="u8"/>
        <member name="b" type="i64"/>
        <member name="c" type="r32"/>
        <member name="d" type="TTypeX"/>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert 1 == len(nodes)
    assert "Struct" == nodes[0].name
    assert [("a", "u8", None, None, None),
            ("b", "i64", None, None, None),
            ("c", "r32", None, None, None),
            ("d", "TTypeX", None, None, None)] == nodes[0].members

def test_struct_parsing_with_constant():
    xml = """\
<x>
    <struct name="Struct">
        <member name="a" type="u8">
            <constant name="THE_CONSTANT" value="0"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [model.Constant("THE_CONSTANT", "0"),
            model.Struct("Struct", [model.StructMember("a", "u8", None, None, None)])] == nodes

def test_struct_parsing_dynamic_array():
    xml = """\
<x>
    <struct name="StructWithDynamic">
        <member name="x" type="TTypeX">
            <dimension isVariableSize="true"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [("x_len", "u32", None, None, None),
            ("x", "TTypeX", True, "x_len", None)] == nodes[0].members

def test_struct_parsing_static_array():
    xml = """\
<x>
    <struct name="StructWithStatic">
        <member name="y" type="TTypeY">
            <dimension size="NUM_OF_Y"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [("y", "TTypeY", True, None, "NUM_OF_Y")] == nodes[0].members

def test_struct_parsing_dynamic_array_with_typed_sizer():
    xml = """\
<x>
    <struct name="StructX">
        <member name="x" type="TTypeX">
            <dimension isVariableSize="true" variableSizeFieldType="TNumberOfItems"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [("x_len", "TNumberOfItems", None, None, None),
            ("x", "TTypeX", True, "x_len", None)] == nodes[0].members

def test_struct_parsing_dynamic_array_with_named_sizer():
    xml = """\
<x>
    <struct name="StructX">
        <member name="x" type="TTypeX">
            <dimension isVariableSize="true" variableSizeFieldName="numOfX"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [("numOfX", "u32", None, None, None),
            ("x", "TTypeX", True, "numOfX", None)] == nodes[0].members

def test_struct_parsing_dynamic_array_with_named_and_typed_sizer():
    xml = """\
<x>
    <struct name="StructX">
        <member name="x" type="TTypeX">
            <dimension isVariableSize="true" variableSizeFieldName="numOfX" variableSizeFieldType="TSize"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [("numOfX", "TSize", None, None, None),
            ("x", "TTypeX", True, "numOfX", None)] == nodes[0].members

def test_struct_parsing_limited_array():
    xml = """\
<x>
    <struct name="StructX">
        <member name="x" type="TTypeX">
            <dimension isVariableSize="true" size="3"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [("x_len", "u32", None, None, None),
            ("x", "TTypeX", True, "x_len", "3")] == nodes[0].members

def test_message_parsing():
    xml = """\
<x>
    <message name="MsgX">
        <member name="x" type="TTypeX"/>
    </message>
</x>
"""
    nodes = parse(xml)

    assert [("x", "TTypeX", None, None, None)] == nodes[0].members

def test_union_parsing():
    xml = """\
<x>
    <union name="Union">
        <member type="A" name="a" discriminatorValue="0"/>
        <member type="B" name="b" discriminatorValue="1"/>
        <member type="C" name="c" discriminatorValue="5"/>
    </union>
</x>
"""
    nodes = parse(xml)

    assert ["Union"] == [node.name for node in nodes]
    assert [("a", "A", "0"), ("b", "B", "1"), ("c", "C", "5")] == nodes[0].members

def test_empty_elemens_parsing():
    xml = """\
<x>
    <typedef name="TILoveTypedefs_ALot"/>
    <enum name="EEnum">
    </enum>
    <struct name="StructX">
    </struct>
    <union name="Union">
    </union>
    <message name="MsgX">
    </message>
</x>
"""

    nodes = parse(xml)

    assert len(nodes) == 0

def test_dependency_sort_enums():
    nodes = [model.Typedef("B", "A"),
             model.Typedef("C", "A"),
             model.Enum("A", [])]

    IsarParser.dependency_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_dependency_sort_typedefs():
    nodes = [model.Typedef("A", "X"),
             model.Typedef("C", "B"),
             model.Typedef("B", "A"),
             model.Typedef("E", "D"),
             model.Typedef("D", "C")]

    IsarParser.dependency_sort(nodes)

    assert ["A", "B", "C", "D", "E"] == [node.name for node in nodes]

def test_dependency_sort_structs():
    nodes = [model.Struct("C", [model.StructMember("a", "B", None, None, None),
                                model.StructMember("b", "A", None, None, None),
                                model.StructMember("c", "D", None, None, None)]),
             model.Struct("B", [model.StructMember("a", "X", None, None, None),
                                model.StructMember("b", "A", None, None, None),
                                model.StructMember("c", "Y", None, None, None)]),
             model.Struct("A", [model.StructMember("a", "X", None, None, None),
                                model.StructMember("b", "Y", None, None, None),
                                model.StructMember("c", "Z", None, None, None)])]

    IsarParser.dependency_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_dependency_sort_struct_with_two_deps():
    nodes = [model.Struct("C", [model.StructMember("a", "B", None, None, None)]),
             model.Struct("B", [model.StructMember("a", "A", None, None, None)]),
             model.Struct("A", [model.StructMember("a", "X", None, None, None)])]

    IsarParser.dependency_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]

def test_dependency_sort_struct_with_multiple_dependencies():
    nodes = [model.Struct("D", [model.StructMember("a", "A", None, None, None),
                                model.StructMember("b", "B", None, None, None),
                                model.StructMember("c", "C", None, None, None)]),
             model.Struct("C", [model.StructMember("a", "A", None, None, None),
                                model.StructMember("b", "B", None, None, None)]),
             model.Struct("B", [model.StructMember("a", "A", None, None, None)]),
             model.Typedef("A", "TTypeX")]

    IsarParser.dependency_sort(nodes)

    assert ["A", "B", "C", "D"] == [node.name for node in nodes]

def test_dependency_sort_union():
    nodes = [model.Typedef("C", "B"),
             model.Union("B", [model.UnionMember("a", "A", "0"),
                               model.UnionMember("b", "A", "1")]),
             model.Struct("A", [model.StructMember("a", "X", None, None, None)])]

    IsarParser.dependency_sort(nodes)

    assert ["A", "B", "C"] == [node.name for node in nodes]
