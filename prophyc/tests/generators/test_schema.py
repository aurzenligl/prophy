# -*- coding: utf-8 -*-

# flake8: noqa W291

import pytest
from prophyc import model

from prophyc.generators import base, schema


@pytest.fixture
def serialize(mocker):
    writes = {}

    def write_mock(file_path, file_content):
        writes.update({file_path: file_content})

    mocker.patch.object(base, '_write_file', side_effect=write_mock)
    mocker.patch.object(base.os.path, 'isdir', return_value=True)

    def process(nodes, gen, base_name='mainer'):
        model.evaluate_model(nodes)
        gen.check_nodes(nodes)
        gen.serialize(nodes, base_name)
        return writes

    return process


@pytest.fixture
def schema_gen(serialize):
    def perform_test(nodes):
        gen = schema.SchemaGenerator()
        writes_ = serialize(nodes, gen, "schema_test")
        assert len(writes_) == 1
        file_names = list(writes_.keys())
        return writes_.get("./schema_test.prophy", "File not written, but: {}".format(file_names[0]))

    return perform_test


def test_empty_tree(schema_gen):
    assert schema_gen([]) == ''


LOREM_W_BREAKS = "\n".join([
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
    "ut labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan "
    "lacus vel facilisis:",
    "  - Dui ut ornare,",
    "  - Lectus,",
    "  - Malesuada pellentesque,",
    "", "",
    "Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas sed.",
    "Neque ornare aenean euismod elementum nisi quis eleifend. Arcu dictum varius duis at "
    "consectetur lorem. Nam at lectus urna duis convallis convallis. At lectus urna duis convallis "
    "convallis tellus. At urna condimentum mattis pellentesque id nibh tortor id. Fames ac turpis.",
    "Egestas integer eget aliquet.",
])


def test_block_comment_level_0():
    assert "".join(schema._gen_multi_line_doc(LOREM_W_BREAKS, max_line_width=100)) == """
/* Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
   labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan lacus 
   vel facilisis:
 * - Dui ut ornare,
 * - Lectus,
 * - Malesuada pellentesque,
 * Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas 
   sed.
 * Neque ornare aenean euismod elementum nisi quis eleifend. Arcu dictum varius duis at consectetur 
   lorem. Nam at lectus urna duis convallis convallis. At lectus urna duis convallis convallis 
   tellus. At urna condimentum mattis pellentesque id nibh tortor id. Fames ac turpis.
 * Egestas integer eget aliquet.
 */"""


def test_block_comment_level_1():
    assert "".join(schema._gen_multi_line_doc(LOREM_W_BREAKS, indent_level=1, block_header="ThatType")) == """
    /* ---- ThatType -------------------------------------------------------------------------------
     * Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
       labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan 
       lacus vel facilisis:
     * - Dui ut ornare,
     * - Lectus,
     * - Malesuada pellentesque,
     * Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas 
       sed.
     * Neque ornare aenean euismod elementum nisi quis eleifend. Arcu dictum varius duis at 
       consectetur lorem. Nam at lectus urna duis convallis convallis. At lectus urna duis convallis 
       convallis tellus. At urna condimentum mattis pellentesque id nibh tortor id. Fames ac turpis.
     * Egestas integer eget aliquet.
     */"""


def test_block_comment_forced_line_overflow():
    text_with_long_word = (
        "Lorem ipsum dolor sit amet, consecteturadipiscingelitseddoeiusmodtempor incididunt ut "
        "labore et dolore magna aliqua. Liberonuncconsequatinterdumvariussit. Maecenas accumsan lacus")

    # test force to overflow if cannot break line into smaller parts
    assert "".join(schema._gen_multi_line_doc(
        text_with_long_word, indent_level=3, block_header="Long block header", max_line_width=40)) == """
            /* Lorem ipsum dolor sit 
               amet, 
               consecteturadipiscingelitseddoeiusmodtempor 
               incididunt ut labore et 
               dolore magna aliqua. 
               Liberonuncconsequatinterdumvariussit. 
               Maecenas accumsan lacus */"""


def test_larger_model(schema_gen):
    input_model = [
        model.Typedef('a', 'i16'),
        model.Typedef('c', 'a'),
        model.Include('some_defs', [
            model.Struct('IncludedStruct', [
                model.StructMember('member1', 'c', 'doc for member1'),
                model.StructMember('member2', 'u32', 'docstring for member1')
            ]),
            model.Typedef('c', 'a'),
        ]),
        model.Union('the_union', [
            model.UnionMember('a', 'IncludedStruct', 0),
            model.UnionMember('field_with_a_long_name', 'Internal', 1, docstring='defined internally'),
            model.UnionMember('other', 'Internal', 4090, docstring='This one has longer discriminator'),
        ], "spec for that union"),
        model.Enum('E1', [
            model.EnumMember('E1_A', '0', 'enum1 constant value A'),
            model.EnumMember('E1_B_has_a_long_name', '1', 'enum1 constant va3lue B'),
            model.EnumMember('E1_C_desc', '2', LOREM_W_BREAKS[:150]),
        ], 'This is Enum E1. It has long description. ' + LOREM_W_BREAKS),
        model.Enum('E2', [
            model.EnumMember('E2_A', '0', "Short\nmultiline\ndoc"),
        ]),
        model.Constant('CONST_A', '6'),
        model.Constant('CONST_B', '0'),
        model.Struct('Internal', [
            model.StructMember('one', 'a', docstring='doc one'),
            model.StructMember('two', 'u32', docstring='doc two')
        ], "Spec for the internally defined structure."),
        model.Struct('Complex', [
            model.StructMember('re', 'i32', docstring='real'),
            model.StructMember('im', 'i32', docstring='imaginary')
        ], "Looks like a complex number"),
    ]

    assert schema_gen(input_model) == '''\
#include "some_defs"


/* Spec for the internally defined structure. */
struct Internal {
    a   one;  // doc one
    u32 two;  // doc two
};


/* spec for that union */
union the_union {
    0:    IncludedStruct a;
    1:    Internal       field_with_a_long_name;  // defined internally
    4090: Internal       other;                   // This one has longer discriminator
};


/* ==== E1 =========================================================================================
 * This is Enum E1. It has long description. Lorem ipsum dolor sit amet, consectetur adipiscing 
   elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Libero nunc consequat 
   interdum varius sit. Maecenas accumsan lacus vel facilisis:
 * - Dui ut ornare,
 * - Lectus,
 * - Malesuada pellentesque,
 * Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas 
   sed.
 * Neque ornare aenean euismod elementum nisi quis eleifend. Arcu dictum varius duis at consectetur 
   lorem. Nam at lectus urna duis convallis convallis. At lectus urna duis convallis convallis 
   tellus. At urna condimentum mattis pellentesque id nibh tortor id. Fames ac turpis.
 * Egestas integer eget aliquet.
 */
enum E1 {
    E1_A                 = 0;  // enum1 constant value A
    E1_B_has_a_long_name = 1;  // enum1 constant va3lue B

    /* Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
       labore et dolore magna aliqua. Libero nunc consequat inte */
    E1_C_desc            = 2;
};


enum E2 {

    /* Short
     * multiline
     * doc */
    E2_A = 0;
};


CONST_A = 6;

CONST_B = 0;


/* Looks like a complex number */
struct Complex {
    i32 re;  // real
    i32 im;  // imaginary
};
'''


def test_constants_layout(schema_gen):
    input_model = [
        model.Constant('CONSTANT_0', "NULL"),
        model.Constant('CONST_D', "1", "This one gets a description."),
        model.Constant('CONST_E', "512"),
        model.Constant('CONSTANT_B', "23", "This one gets longer description. " * 4),
        model.Constant('CONST_C', "NO DESC"),
        model.Constant('D', "CONSTANT_B"),
    ]

    assert schema_gen(input_model) == '''\

CONSTANT_0 = NULL;

CONST_D = 1;  // This one gets a description.

CONST_E = 512;


/* This one gets longer description. This one gets longer description. This one gets longer 
   description. This one gets longer description. */
CONSTANT_B = 23;

CONST_C = NO DESC;

D = CONSTANT_B;
'''


def test_container_layout(schema_gen):
    input_model = [
        model.Struct('StaticVectors', [
            model.StructMember('ext_size', 'i16', docstring='arbitrary sizer for dynamic arrays'),
            model.StructMember('optional_element', 'Complex', optional=True, docstring='optional array'),
            model.StructMember('fixed', 'Complex', size=3, docstring='static size array'),
            model.StructMember('samples', 'Complex', bound='ext_size', docstring='limited (ext.sized) array 1'),
            model.StructMember('dyn_array', 'i16', bound='num_of_dyn_array', docstring='dynamic array'),
            model.StructMember('scalings', 'r64', bound='ext_size', docstring='limited (ext.sized) array 2'),
            model.StructMember('dynamic', 'UeEntry', bound='sizer', docstring='dynamic array'),
        ], LOREM_W_BREAKS),

        model.Struct('UeEntry', [
            model.StructMember('frame', 'u16'),
            model.StructMember('subframe', 'u8', docstring="Short info."),
            model.StructMember('symbol', 'u8',
                               docstring="This is the only one field that gets a long description in this structure. "
                                         "The info is too long to fit in one line."),
            model.StructMember('context', 'r32', size=16),

        ], "Short UeEntry description"),

        model.Struct('DynamicSizeVector', [
            model.StructMember('sizer', 'i16', docstring='sizer field for dynamic arrays'),
            model.StructMember('dynamic', 'Complex', bound='sizer', docstring='dynamic array'),
            model.StructMember('greedy', 'Complex', unlimited=True, docstring='greedy array'),
        ], "This one has shorter description."),
    ]

    assert schema_gen(input_model) == '''\

/* Short UeEntry description */
struct UeEntry {
    u16 frame;
    u8  subframe;     // Short info.

    /* This is the only one field that gets a long description in this structure. The info is too 
       long to fit in one line. */
    u8  symbol;
    r32 context[16];
};


/* ==== StaticVectors ==============================================================================
 * Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut 
   labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan lacus 
   vel facilisis:
 * - Dui ut ornare,
 * - Lectus,
 * - Malesuada pellentesque,
 * Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas 
   sed.
 * Neque ornare aenean euismod elementum nisi quis eleifend. Arcu dictum varius duis at consectetur 
   lorem. Nam at lectus urna duis convallis convallis. At lectus urna duis convallis convallis 
   tellus. At urna condimentum mattis pellentesque id nibh tortor id. Fames ac turpis.
 * Egestas integer eget aliquet.
 */
struct StaticVectors {
    i16      ext_size;                      // arbitrary sizer for dynamic arrays
    Complex* optional_element;              // optional array
    Complex  fixed[3];                      // static size array
    Complex  samples<@ext_size>;            // limited (ext.sized) array 1
    i16      dyn_array<@num_of_dyn_array>;  // dynamic array
    r64      scalings<@ext_size>;           // limited (ext.sized) array 2
    UeEntry  dynamic<@sizer>;               // dynamic array
};


/* This one has shorter description. */
struct DynamicSizeVector {
    i16     sizer;            // sizer field for dynamic arrays
    Complex dynamic<@sizer>;  // dynamic array
    Complex greedy<...>;      // greedy array
};
'''
