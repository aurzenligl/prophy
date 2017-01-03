import pytest

from prophyc import model
from prophyc.parsers.isar import IsarParser
from prophyc.parsers.isar import expand_operators
from prophyc.file_processor import CyclicIncludeError, FileNotFoundError

def parse(xml_string, process_file = lambda path: [], warn = None):
    return IsarParser(warn = warn).parse(xml_string, '', process_file)

def test_includes_parsing():
    xml = """\
<system xmlns:xi="http://www.xyz.com/1984/XInclude">
    <xi:include href="mydlo.xml"/>
    <xi:include href="szydlo.xml"/>
    <xi:include href="powidlo.xml"/>
    <xi:include href="../zurawina.xml"/>
    <xi:include href="../entliczek/petliczek.xml"/>
    <xi:include href="../my.basename.xml"/>
    <xi:include href="noext"/>
</system>
"""
    nodes = parse(xml, process_file = lambda path: [model.Typedef("a", "u8")])

    assert [
        ("mydlo", [model.Typedef("a", "u8")]),
        ("szydlo", [model.Typedef("a", "u8")]),
        ("powidlo", [model.Typedef("a", "u8")]),
        ("../zurawina", [model.Typedef("a", "u8")]),
        ("../entliczek/petliczek", [model.Typedef("a", "u8")]),
        ("../my.basename", [model.Typedef("a", "u8")]),
        ("noext", [model.Typedef("a", "u8")]),
    ] == nodes

def test_includes_call_file_process_with_proper_path():
    xml = """\
<system xmlns:xi="http://www.xyz.com/1984/XInclude">
    <xi:include href="input.xml"/>
</system>
"""
    processed_paths = []

    def process_file(path):
        processed_paths.append(path)
        return []

    parse(xml, process_file = process_file)

    assert processed_paths == ['input.xml']

def test_includes_cyclic_include_error():
    xml = """\
<system xmlns:xi="http://www.xyz.com/1984/XInclude">
    <xi:include href="input.xml"/>
</system>
"""

    def process_file_with_error(path):
        raise CyclicIncludeError(path)
    warnings = []

    nodes = parse(
        xml,
        process_file = process_file_with_error,
        warn = lambda msg: warnings.append(msg))

    assert nodes == [('input', [])]
    assert warnings == ['file input.xml included again during parsing']

def test_includes_file_not_found_error():
    xml = """\
<system xmlns:xi="http://www.xyz.com/1984/XInclude">
    <xi:include href="input.xml"/>
</system>
"""

    def process_file_with_error(path):
        raise FileNotFoundError(path)
    warnings = []

    nodes = parse(
        xml,
        process_file = process_file_with_error,
        warn = lambda msg: warnings.append(msg))

    assert nodes == [('input', [])]
    assert warnings == ['file input.xml not found']

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
    assert parse(xml) == [
        model.Typedef("a", "u8"),
        model.Typedef("b", "u16"),
        model.Typedef("c", "u32"),
        model.Typedef("d", "u64"),
        model.Typedef("e", "i8"),
        model.Typedef("f", "i16"),
        model.Typedef("g", "i32"),
        model.Typedef("h", "i64"),
        model.Typedef("i", "r32"),
        model.Typedef("j", "r64")
    ]

def test_typedefs_parsing():
    xml = """\
<x>
    <typedef name="TILoveTypedefs_ALot" type="MyType"/>
</x>
"""
    assert parse(xml) == [model.Typedef("TILoveTypedefs_ALot", "MyType")]

def test_enums_parsing():
    xml = """\
<x>
    <enum name="EEnum">
        <enum-member name="EEnum_A" value="0"/>
        <enum-member name="EEnum_B" value="1"/>
        <enum-member name="EEnum_C" value="-1"/>
        <enum-member name="EEnum_D" value="-10"/>
    </enum>
</x>
"""
    assert parse(xml) == [
        model.Enum("EEnum", [
            model.EnumMember("EEnum_A", "0"),
            model.EnumMember("EEnum_B", "1"),
            model.EnumMember("EEnum_C", "0xFFFFFFFF"),
            model.EnumMember("EEnum_D", "0xFFFFFFF6"),
        ])
    ]

def test_enums_parsing_repeated_value():
    xml = """\
<x>
    <enum name="EEnum">
        <enum-member name="EEnum_D" value="-10"/>
        <enum-member name="EEnum_D2" value="0xFFFFFFF6"/>
    </enum>
</x>
"""
    with pytest.raises(ValueError) as e:
        parse(xml)
    assert "Duplicate Enum value" in str(e)

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

    assert parse(xml) == [
        model.Struct("Struct", [
            model.StructMember("a", "u8"),
            model.StructMember("b", "i64"),
            model.StructMember("c", "r32"),
            model.StructMember("d", "TTypeX")
        ])
    ]

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
    assert parse(xml) == [
        model.Constant("THE_CONSTANT", "0"),
        model.Struct("Struct", [model.StructMember("a", "u8")])
    ]

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
    assert parse(xml) == [
        model.Struct("StructWithDynamic", [
            model.StructMember("x_len", "u32"),
            model.StructMember("x", "TTypeX", bound = "x_len")
        ])
    ]

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
    assert parse(xml) == [
        model.Struct("StructWithStatic", [
            model.StructMember("y", "TTypeY", size = "NUM_OF_Y")
        ])
    ]

def test_struct_parsing_static_2d_array():
    xml = """\
<x>
    <struct name="StructWithStatic">
        <member name="y" type="TTypeY">
            <dimension size="NUM_OF_Y" size2="NUM_OF_X"/>
        </member>
    </struct>
</x>
"""
    assert parse(xml) == [
        model.Struct("StructWithStatic", [
            model.StructMember("y", "TTypeY", size = "NUM_OF_Y*NUM_OF_X")
        ])
    ]

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
    assert parse(xml) == [
        model.Struct("StructX", [
            model.StructMember("x_len", "TNumberOfItems"),
            model.StructMember("x", "TTypeX", bound = "x_len")
        ])
    ]

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
    assert parse(xml) == [
        model.Struct("StructX", [
            model.StructMember("numOfX", "u32"),
            model.StructMember("x", "TTypeX", bound = "numOfX")
        ])
    ]

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
    assert parse(xml) == [
        model.Struct("StructX", [
            model.StructMember("numOfX", "TSize"),
            model.StructMember("x", "TTypeX", bound = "numOfX")
        ])
    ]

def test_isar_struct_parsing_ext_sized_array():
    xml = """\
<x>
    <struct name="StructX">
        <member name="a" type="u8"/>
        <member name="numOfZzz" type="u16"/>
        <member name="prophy_styled_x" type="u16">
            <dimension isVariableSize="true" variableSizeFieldName="@a"/>
        </member>
        <member name="prophy_styled_y" type="u16">
            <dimension isVariableSize="true" variableSizeFieldName="@a"/>
        </member>
        <member name="nativeIsarDefined" type="u32">
            <dimension size="THIS_IS_VARIABLE_SIZE_ARRAY"/>
        </member>
    </struct>
</x>
"""
    assert parse(xml) == [
        model.Struct("StructX", [
            model.StructMember("a", "u8"),
            model.StructMember("numOfZzz", "u16"),
            model.StructMember("prophy_styled_x", "u16", bound = "a"),
            model.StructMember("prophy_styled_y", "u16", bound = "a"),
            model.StructMember("nativeIsarDefined", "u32", bound = "numOfNativeIsarDefined")
        ])
    ]

def test_isar_message_parsing_with_ext_sized_arrays():
    xml = """\
<x>
    <component name="ULPHY_MAC">
        <definitions>
             <typedef comment="some comment" name="DefA" type="u16"/>
             <typedef comment="some comment" name="DefB" type="i32"/>
        </definitions>
        <message name="StructX">
            <member name="a" type="u8"/>
            <member name="numOfZzz" type="u16"/>
            <member name="prophy_styled_x" type="u16">
                <dimension isVariableSize="true" variableSizeFieldName="@a"/>
            </member>
            <member name="prophy_styled_y" type="DefA">
                <dimension isVariableSize="true" variableSizeFieldName="@a"/>
            </member>
            <member name="nativeIsarDefined" type="DefA">
                <dimension size="THIS_IS_VARIABLE_SIZE_ARRAY"/>
            </member>
            <member name="dummy" type="DefB"/>
        </message>
    </component>
</x>
"""
    assert parse(xml) == [
        model.Typedef("DefA", "u16"),
        model.Typedef("DefB", "i32"),
        model.Struct("StructX", [
            model.StructMember("a", "u8"),
            model.StructMember("numOfZzz", "u16"),
            model.StructMember("prophy_styled_x", "u16", bound = "a"),
            model.StructMember("prophy_styled_y", "DefA", bound = "a"),
            model.StructMember("nativeIsarDefined", "DefA", bound = "numOfNativeIsarDefined"),
            model.StructMember("dummy", "DefB")
        ])
    ]

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
    assert parse(xml) == [
        model.Struct("StructX", [
            model.StructMember("x_len", "u32"),
            model.StructMember("x", "TTypeX", bound = "x_len", size = "3")
        ])
    ]

def test_struct_parsing_with_optional():
    xml = """\
<x>
    <struct name="Struct">
        <member name="a" type="u8" optional="true"/>
        <member name="b" type="u8" optional="false"/>
    </struct>
</x>
"""
    assert parse(xml) == [
        model.Struct("Struct", [
            model.StructMember("a", "u8", optional = True),
            model.StructMember("b", "u8", optional = False)
        ])
    ]

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
    assert parse(xml) == [
        model.Struct("X", [
            model.StructMember("has_a", "u32"),
            model.StructMember("a_len", "u32"),
            model.StructMember("a", "A", bound = "a_len", size = "5")
        ])
    ]

def test_message_parsing():
    xml = """\
<x>
    <message name="MsgX">
        <member name="x" type="TTypeX"/>
    </message>
</x>
"""
    assert parse(xml) == [
        model.Struct("MsgX", [
            model.StructMember("x", "TTypeX")
        ])
    ]

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
    assert parse(xml) == [
        model.Struct("X", [
            model.StructMember("a_len", "u32"),
            model.StructMember("a", "A", bound = "a_len", size = "5")
        ]),
        model.Struct("Y", [
            model.StructMember("b_len", "u32"),
            model.StructMember("b", "B", bound = "b_len")
        ])
    ]

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
    assert nodes[0].members == [
        model.UnionMember("a", "A", "0"),
        model.UnionMember("b", "B", "1"),
        model.UnionMember("c", "C", "5")
    ]

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
    assert parse(xml) == [model.Typedef("ImNotAPrimitiveType", "u32")]

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
        (model.Enum("Enum", [
            model.EnumMember("Enum_A", "((Constant) << (16))")
        ]))
    ]
    assert nodes[1].members[0].value == "((Constant) << (16))"
