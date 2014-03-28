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
    holder = parse(xml)

    assert ["mydlo", "szydlo", "powidlo"] == holder.includes

def test_constants_parsing():
    xml = """\
<x>
    <constant name="CONST_A" value="0"/>
    <constant name="CONST_B" value="31"/>
</x>
"""
    holder = parse(xml)

    assert [("CONST_A", "0"), ("CONST_B", "31")] == holder.constants

def test_constants_parsing_and_sorting():
    xml = """\
<x>
    <constant name="C_A" value="C_B + C_C"/>
    <constant name="C_B" value="1"/>
    <constant name="C_C" value="2"/>
</x>
"""
    holder = parse(xml)

    assert [("C_B", "1"), ("C_C", "2"), ("C_A", "C_B + C_C")] == holder.constants

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
    holder = parse(xml)

    assert [("a", "u8"),
            ("b", "u16"),
            ("c", "u32"),
            ("d", "u64"),
            ("e", "i8"),
            ("f", "i16"),
            ("g", "i32"),
            ("h", "i64"),
            ("i", "r32"),
            ("j", "r64")] == holder.typedefs

def test_typedefs_parsing():
    xml = """<typedef name="TILoveTypedefs_ALot" type="MyType"/>"""
    holder = parse(xml)

    assert [("TILoveTypedefs_ALot", "MyType")] == holder.typedefs

def test_enums_parsing():
    xml = """\
<enum name="EEnum">
    <enum-member name="EEnum_A" value="0"/>
    <enum-member name="EEnum_B" value="1"/>
    <enum-member name="EEnum_C" value="-1"/>
</enum>
"""
    holder = parse(xml)

    assert 1 == len(holder.enums)
    assert "EEnum" == holder.enums[0][0]
    assert [("EEnum_A", "0"), ("EEnum_B", "1"), (u"EEnum_C", "0xFFFFFFFF")] == holder.enums[0][1]

def test_struct_parsing():
    xml = """\
<struct name="Struct">
    <member name="a" type="u8"/>
    <member name="b" type="i64"/>
    <member name="c" type="r32"/>
    <member name="d" type="TTypeX"/>
</struct>
"""
    holder = parse(xml)

    assert 1 == len(holder.structs)
    assert "Struct" == holder.structs[0].name
    assert [("a", "u8", None, None, None),
            ("b", "i64", None, None, None),
            ("c", "r32", None, None, None),
            ("d", "TTypeX", None, None, None)] == holder.structs[0].members

def test_struct_parsing_dynamic_array():
    xml = """\
<struct name="StructWithDynamic">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert [("x_len", "u32", None, None, None),
            ("x", "TTypeX", True, "x_len", None)] == holder.structs[0].members

def test_struct_parsing_static_array():
    xml = """\
<struct name="StructWithStatic">
    <member name="y" type="TTypeY">
        <dimension size="NUM_OF_Y"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert [("y", "TTypeY", True, None, "NUM_OF_Y")] == holder.structs[0].members

def test_struct_parsing_dynamic_array_with_typed_sizer():
    xml = """\
<struct name="StructX">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true" variableSizeFieldType="TNumberOfItems"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert [("x_len", "TNumberOfItems", None, None, None),
            ("x", "TTypeX", True, "x_len", None)] == holder.structs[0].members

def test_struct_parsing_dynamic_array_with_named_sizer():
    xml = """\
<struct name="StructX">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true" variableSizeFieldName="numOfX"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert [("numOfX", "u32", None, None, None),
            ("x", "TTypeX", True, "numOfX", None)] == holder.structs[0].members

def test_struct_parsing_dynamic_array_with_named_and_typed_sizer():
    xml = """\
<struct name="StructX">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true" variableSizeFieldName="numOfX" variableSizeFieldType="TSize"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert [("numOfX", "TSize", None, None, None),
            ("x", "TTypeX", True, "numOfX", None)] == holder.structs[0].members

def test_message_parsing():
    xml = """\
<message name="MsgX">
    <member name="x" type="TTypeX"/>
</message>
"""
    holder = parse(xml)

    assert [("x", "TTypeX", None, None, None)] == holder.structs[0].members
