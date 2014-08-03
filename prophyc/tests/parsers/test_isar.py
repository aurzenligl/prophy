from prophyc import model
from prophyc.parsers.isar import IsarParser
from prophyc.parsers.isar import expand_operators

def parse(xml_string):
    return IsarParser().parse_string(xml_string)

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
    assert [("a", "u8", None, None, None, False),
            ("b", "i64", None, None, None, False),
            ("c", "r32", None, None, None, False),
            ("d", "TTypeX", None, None, None, False)] == nodes[0].members

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
            model.Struct("Struct", [model.StructMember("a", "u8", None, None, None, False)])] == nodes

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

    assert [("x_len", "u32", None, None, None, False),
            ("x", "TTypeX", True, "x_len", None, False)] == nodes[0].members

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

    assert [("y", "TTypeY", True, None, "NUM_OF_Y", False)] == nodes[0].members

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

    assert [("x_len", "TNumberOfItems", None, None, None, False),
            ("x", "TTypeX", True, "x_len", None, False)] == nodes[0].members

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

    assert [("numOfX", "u32", None, None, None, False),
            ("x", "TTypeX", True, "numOfX", None, False)] == nodes[0].members

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

    assert [("numOfX", "TSize", None, None, None, False),
            ("x", "TTypeX", True, "numOfX", None, False)] == nodes[0].members

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

    assert [("x_len", "u32", None, None, None, False),
            ("x", "TTypeX", True, "x_len", "3", False)] == nodes[0].members

def test_struct_parsing_with_optional():
    xml = """\
<x>
    <struct name="Struct">
        <member name="a" type="u8" optional="true"/>
    </struct>
</x>
"""

    nodes = parse(xml)

    assert [("a", "u8", None, None, None, True)] == nodes[0].members

def test_struct_parsing_with_optional_array():
    xml = """\
<x>
    <struct name="X">
        <member name="a" optional="true" type="A">
            <dimension isVariableSize="true" size="5"/>
        </member>
    </struct>
</x>
"""
    nodes = parse(xml)

    assert [("has_a", "u32", None, None, None, False),
            ("a_len", "u32", None, None, None, False),
            ("a", "A", True, "a_len", "5", False)] == nodes[0].members

def test_message_parsing():
    xml = """\
<x>
    <message name="MsgX">
        <member name="x" type="TTypeX"/>
    </message>
</x>
"""
    nodes = parse(xml)

    assert [("x", "TTypeX", None, None, None, False)] == nodes[0].members

def test_struct_and_message_with_dynamic_array_parsing():
    xml = """\
<x>
    <struct name="X">
        <member name="a" type="A">
            <dimension isVariableSize="true" size="5"/>
        </member>
    </struct>
    <message name="Y">
        <member name="b" type="B">
            <dimension isVariableSize="true" size="5"/>
        </member>
    </message>
</x>"""

    nodes = parse(xml)

    assert [('a_len', 'u32', None, None, None, False),
            ('a', 'A', True, 'a_len', '5', False)] == nodes[0].members
    assert [('b_len', 'u32', None, None, None, False),
            ('b', 'B', True, 'b_len', None, False)] == nodes[1].members

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

def test_primitive_types():
    xml = """\
<xml>
    <typedef name="u8" primitiveType="8 bit integer unsigned"/>
    <typedef name="u16" primitiveType="16 bit integer unsigned"/>
    <typedef name="u32" primitiveType="32 bit integer unsigned"/>
    <typedef name="u64" primitiveType="64 bit integer unsigned"/>
    <typedef name="i8" primitiveType="8 bit integer signed"/>
    <typedef name="i16" primitiveType="16 bit integer signed"/>
    <typedef name="i32" primitiveType="32 bit integer signed"/>
    <typedef name="i64" primitiveType="64 bit integer signed"/>
    <typedef name="ImNotAPrimitiveType" primitiveType="32 bit integer unsigned"/>
    <typedef name="r32" primitiveType="32 bit float"/>
    <typedef name="r64" primitiveType="64 bit float"/>
</xml>
"""

    nodes = parse(xml)

    assert nodes == [("ImNotAPrimitiveType", "u32")]

def test_operator_expansion():
    assert expand_operators('bitMaskOr(1, 2)') == '((1) | (2))'
    assert expand_operators('shiftLeft(1, 2)') == '((1) << (2))'

    assert expand_operators('bitMaskOr(1 ,2)') == '((1) | (2))'
    assert expand_operators('bitMaskOr(1 , 2)') == '((1) | (2))'

    assert (expand_operators('shiftLeft(bitMaskOr(1, 2), bitMaskOr(3, 4))') ==
                '((((1) | (2))) << (((3) | (4))))')

def test_operator_expansion_in_enum_and_constant():
    xml = """\
<x>
    <constant name="Constant" value="bitMaskOr(value_one, value_two)"/>
    <enum name="Enum">
        <enum-member name="Enum_A" value="shiftLeft(Constant, 16)"/>
    </enum>
</x>
"""

    nodes = parse(xml)

    assert nodes == [
        ("Constant", "((value_one) | (value_two))"),
        ("Enum", [
            ("Enum_A", "((Constant) << (16))")
        ])
    ]
