# -*- coding: utf-8 -*-

import DataHolder
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
    assert 4 == len(holder.structs[0].members)
    assert "Struct" == holder.structs[0].name
    assert "a" == holder.structs[0].members[0].name
    assert "u8" == holder.structs[0].members[0].type
    assert None == holder.structs[0].members[0].array
    assert "b" == holder.structs[0].members[1].name
    assert "i64" == holder.structs[0].members[1].type
    assert None == holder.structs[0].members[1].array
    assert "c" == holder.structs[0].members[2].name
    assert "r32" == holder.structs[0].members[2].type
    assert None == holder.structs[0].members[2].array
    assert "d" == holder.structs[0].members[3].name
    assert "TTypeX" == holder.structs[0].members[3].type
    assert None == holder.structs[0].members[3].array

def test_struct_parsing_dynamic_array():
    xml = """\
<struct name="StructWithDynamic">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert 1 == len(holder.structs)
    assert 2 == len(holder.structs[0].members)
    assert "StructWithDynamic" == holder.structs[0].name
    assert "x_len" == holder.structs[0].members[0].name
    assert "u32" == holder.structs[0].members[0].type
    assert "x" == holder.structs[0].members[1].name
    assert "TTypeX" == holder.structs[0].members[1].type
    assert True == holder.structs[0].members[1].array
    assert "x_len" == holder.structs[0].members[1].array_bound
    assert None == holder.structs[0].members[1].array_size

def test_struct_parsing_static_array():
    xml = """\
<struct name="StructWithStatic">
    <member name="y" type="TTypeY">
        <dimension size="NUM_OF_Y"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert 1 == len(holder.structs)
    assert 1 == len(holder.structs[0].members)
    assert "StructWithStatic" == holder.structs[0].name
    assert "y" == holder.structs[0].members[0].name
    assert "TTypeY" == holder.structs[0].members[0].type
    assert True == holder.structs[0].members[0].array
    assert None == holder.structs[0].members[0].array_bound
    assert "NUM_OF_Y" == holder.structs[0].members[0].array_size

# <dimension isVariableSize="true" size="MAX_NUM_DRB_PER_USER" variableSizeFieldName="numDrbs" variableSizeFieldType="TNumberOfItems"/>

def test_struct_parsing_dynamic_array_with_typed_sizer():
    xml = """\
<struct name="StructX">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true" variableSizeFieldType="TNumberOfItems"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert 1 == len(holder.structs)
    assert 2 == len(holder.structs[0].members)
    assert "StructX" == holder.structs[0].name
    assert "x_len" == holder.structs[0].members[0].name
    assert "TNumberOfItems" == holder.structs[0].members[0].type
    assert None == holder.structs[0].members[0].array
    assert "x" == holder.structs[0].members[1].name
    assert "TTypeX" == holder.structs[0].members[1].type
    assert True == holder.structs[0].members[1].array
    assert "x_len" == holder.structs[0].members[1].array_bound
    assert None == holder.structs[0].members[1].array_size

def test_struct_parsing_dynamic_array_with_named_sizer():
    xml = """\
<struct name="StructX">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true" variableSizeFieldName="numOfX"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert 2 == len(holder.structs[0].members)
    assert "numOfX" == holder.structs[0].members[0].name
    assert "u32" == holder.structs[0].members[0].type
    assert "x" == holder.structs[0].members[1].name
    assert "TTypeX" == holder.structs[0].members[1].type
    assert True == holder.structs[0].members[1].array
    assert "numOfX" == holder.structs[0].members[1].array_bound
    assert None == holder.structs[0].members[1].array_size

def test_struct_parsing_dynamic_array_with_named_and_typed_sizer():
    xml = """\
<struct name="StructX">
    <member name="x" type="TTypeX">
        <dimension isVariableSize="true" variableSizeFieldName="numOfX" variableSizeFieldType="TSize"/>
    </member>
</struct>
"""
    holder = parse(xml)

    assert 2 == len(holder.structs[0].members)
    assert "numOfX" == holder.structs[0].members[0].name
    assert "TSize" == holder.structs[0].members[0].type
    assert "x" == holder.structs[0].members[1].name
    assert "TTypeX" == holder.structs[0].members[1].type
    assert True == holder.structs[0].members[1].array
    assert "numOfX" == holder.structs[0].members[1].array_bound
    assert None == holder.structs[0].members[1].array_size
