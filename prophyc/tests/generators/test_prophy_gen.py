# -*- coding: utf-8 -*-

# flake8: noqa W291

import pytest
from prophyc import model

from prophyc.generators import base, prophy


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
        gen = prophy.SchemaGenerator()
        writes_ = serialize(nodes, gen, "schema_test")
        assert len(writes_) == 1
        file_names = list(writes_.keys())
        return writes_.get("./schema_test.prophy", "File not written, but: {}".format(file_names[0]))

    return perform_test


def test_empty_tree(schema_gen):
    assert schema_gen([]) == ''


def test_structs(schema_gen):
    model_nodes = [
        model.Struct('X', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u64', size=2),
        ]),
        model.Struct('Y', [
            model.StructMember('q', 'u16'),
        ]),
    ]
    assert schema_gen(model_nodes) == """\
struct X {
    u32 x;
    u64 y[2];
};


struct Y {
    u16 q;
};
"""


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


def test_larger_model(schema_gen, larger_model):
    assert schema_gen(larger_model) == """\
#include "some_defs"
#include "cplx"

/* the_union
 * spec for that union
 */
union the_union {
    0:    IncludedStruct a;
    1:    cint16_t       field_with_a_long_name;    // Shorter
    2:    cint32_t       field_with_a_longer_name;  // Longer description
    4090: i32            other;                     // This one has larger discriminator
};


/* E1
 * Enumerator is a model type that is not supposed to be serialized. Its definition represents yet
   another syntax variation for typing a constant. Of course elements of it's type are serializable
   (as int32)
 */
enum E1 {
    E1_A                 = 0;  // enum1 constant value A
    E1_B_has_a_long_name = 1;  // enum1 constant va3lue B
    /* E1_C_desc
     * Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
       labore et dolore magna aliqua. Libero nunc consequat inte
     */
    E1_C_desc            = 2;
};


enum E2 {
    /* E2_A
     * Short
     * multiline
     * doc
     */
    E2_A = 0;
};


CONST_A = 6;

CONST_B = 0;


/* ==== StructMemberKinds ==========================================================================
 * StructMemberKinds
 * Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
   labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan lacus
   vel facilisis:
 *    - Dui ut ornare,
 *    - Lectus,
 *    - Malesuada pellentesque,
 * Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas
   sed.
 * Egestas integer eget aliquet.
 */
struct StructMemberKinds {
    i16       member_without_docstring;
    i16       ext_size;                  // arbitrary sizer for dynamic arrays
    cint16_t* optional_element;          // optional array
    cint16_t  fixed_array[3];            // Array with static size.
    cint16_t  samples<@ext_size>;        // dynamic (ext.sized) array
    r64       limited_array<4>;          // Has statically evaluable maximum size.
    /* greedy
     * Represents array of arbitrary number of elements. Buffer size must be multiply of element
       size.
     */
    cint16_t  greedy<...>;
};
"""


def test_constants_layout(schema_gen):
    input_model = [
        model.Constant('CONSTANT_0', "NULL"),
        model.Constant('CONST_D', "1", "This one gets a description."),
        model.Constant('CONST_E', "512"),
        model.Constant('CONSTANT_B', "23", "This one gets longer description. " * 4),
        model.Constant('CONST_C', "NO DESC"),
        model.Constant('D', "CONSTANT_B"),
    ]

    assert schema_gen(input_model) == """\

CONSTANT_0 = NULL;

CONST_D = 1;  // This one gets a description.

CONST_E = 512;

/* CONSTANT_B
 * This one gets longer description. This one gets longer description. This one gets longer
   description. This one gets longer description. 
 */
CONSTANT_B = 23;

CONST_C = NO DESC;

D = CONSTANT_B;
"""
