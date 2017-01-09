import os
import tempfile
import pytest

from prophyc import patch
from prophyc import model

def parse(content):
    try:
        with tempfile.NamedTemporaryFile(delete = False) as temp:
            temp.write(content)
            temp.flush()
            return patch.parse(temp.name)
    finally:
        os.unlink(temp.name)

def test_parsing_ignoring_empty_lines():
    content = b"""\

MyStruct type lastField MyRealMember

YourStruct type firstField YourRealMember
YourStruct type lastField AnotherRealMember

"""

    patches = parse(content)

    assert {'MyStruct': [('type', ['lastField', 'MyRealMember'])],
            'YourStruct': [('type', ['firstField', 'YourRealMember']),
                           ('type', ['lastField', 'AnotherRealMember'])]} == patches

def test_unknown_action():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('typo_or_something', [])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Unknown action: MyStruct Action(action='typo_or_something', params=[])" == str(e.value)

def test_change_field_type():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('type', ['field2', 'TheRealType'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('field2', 'TheRealType'),
                                      model.StructMember('field3', 'u32')])] == nodes

def test_change_field_type_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('type', ['field2', 'TheRealType'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct Action(action='type', params=['field2', 'TheRealType'])" == str(e.value)

def test_change_field_type_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('type', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

    patches = {'MyStruct': [patch.Action('type', ['field2', 'TheRealType', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

def test_change_field_type_member_not_found():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('type', ['field4', 'TheRealType'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in str(e.value)

def test_insert_field():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8']),
                            patch.Action('insert', ['-1', 'additional2', 'u16']),
                            patch.Action('insert', ['128', 'additional3', 'u64'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('additional1', 'u8'),
                                      model.StructMember('field2', 'u32'),
                                      model.StructMember('additional2', 'u16'),
                                      model.StructMember('field3', 'u32'),
                                      model.StructMember('additional3', 'u64')])] == nodes

def test_insert_field_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Can insert field only in struct: MyStruct' in str(e.value)

def test_insert_field_no_3_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8', 'extra'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 3 params: MyStruct' in str(e.value)

def test_insert_field_index_not_an_int():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('insert', ['not_a_number', 'additional1', 'u8'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Index is not a number: MyStruct' in str(e.value)

def test_remove_field():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('remove', ['field2'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('field3', 'u32')])] == nodes

def test_remove_field_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('remove', ['field2'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Can remove field only in struct: MyStruct' in str(e.value)

def test_remove_field_no_1_param():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('remove', ['field1', 'extra_param'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Remove field must have 1 param: MyStruct' in str(e.value)

def test_remove_field_not_found():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('remove', ['not_a_field'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in str(e.value)

def test_make_field_dynamic_array():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('dynamic', ['field3', 'field1'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('field2', 'u32'),
                                      model.StructMember('field3', 'u32', bound = 'field1')])] == nodes

def test_make_field_dynamic_array_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('dynamic', ['field2', 'field1'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct" in str(e.value)

def test_make_field_dynamic_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('dynamic', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

    patches = {'MyStruct': [patch.Action('dynamic', ['field2', 'field1', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

def test_make_field_dynamic_array_member_not_found():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('dynamic', ['field4', 'field1'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in str(e.value)

def test_make_field_greedy_array():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('greedy', ['field3'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('field2', 'u32'),
                                      model.StructMember('field3', 'u32', unlimited = True)])] == nodes

def test_make_field_greedy_array_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('greedy', ['field2'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct" in str(e.value)

def test_make_field_greedy_array_no_1_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('greedy', ['field2', 'extra_args'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 1 params: MyStruct' in str(e.value)


def test_make_field_greedy_array_with_wrong_name_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('greedy', ['field4'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in str(e.value)

def test_make_field_static_array():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('static', ['field3', '3'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('field2', 'u32'),
                                      model.StructMember('field3', 'u32', size = '3')])] == nodes

def test_make_field_static_array_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('static', ['field2', '3'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct" in str(e.value)

def test_make_field_static_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('static', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

    patches = {'MyStruct': [patch.Action('static', ['field2', '3', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

def test_make_field_static_array_with_wrong_name_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('static', ['field4', '3'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in str(e.value)

def test_make_field_limited_array():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32", size = '20')])]
    patches = {'MyStruct': [patch.Action('limited', ['field3', 'field2'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('field2', 'u32'),
                                      model.StructMember('field3', 'u32', bound = 'field2', size = '20')])] == nodes

def test_make_field_limited_array_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('limited', ['field3', 'field2'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct" in str(e.value)

def test_make_field_limited_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('limited', ['field3'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

    patches = {'MyStruct': [patch.Action('limited', ['field3', 'field2', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in str(e.value)

def test_make_field_limited_array_with_wrong_name_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('limited', ['field4', 'field2'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in str(e.value)

def test_make_field_limited_array_with_wrong_bound_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('limited', ['field3', 'field4'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Array len member not found: MyStruct' in str(e.value)

def test_change_union_to_struct():
    nodes = [model.Union("MyUnion", [model.UnionMember("field1", "u32", 1)])]
    patches = {'MyUnion': [patch.Action('struct', [])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyUnion', [model.StructMember('field1', 'u32')])] == nodes

def test_change_union_to_struct_and_remove_field():
    nodes = [model.Union("MyUnion", [model.UnionMember("field1", "u32", 1),
                                     model.UnionMember("field2", "u32", 2),
                                     model.UnionMember("field3", "u32", 3)])]

    patches = {'MyUnion': [patch.Action('struct', []),
                           patch.Action('remove', ['field2'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyUnion', [model.StructMember('field1', 'u32'),
                                     model.StructMember('field3', 'u32')])] == nodes

def test_change_union_to_struct_not_a_union():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", 1),
                                       model.StructMember("field2", "u32", 2)])]
    patches = {'MyStruct': [patch.Action('struct', [])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Can only change union to struct: MyStruct' in str(e.value)

def test_change_union_to_struct_excessive_params():
    nodes = [model.Union("MyUnion", [model.UnionMember("field1", "u32", 1),
                                     model.UnionMember("field2", "u32", 2)])]
    patches = {'MyUnion': [patch.Action('struct', ['surplus_param'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change union to struct takes no params: MyUnion' in str(e.value)

def test_rename_node():
    nodes = [model.Struct("OldStruct", [model.StructMember("field", "u32")]),
             model.Enum("OldEnum", [model.EnumMember("val", "123")])]

    patches = {'OldStruct': [patch.Action('rename', ['NewStruct'])],
               'OldEnum': [patch.Action('rename', ['NewEnum'])]}

    patch.patch(nodes, patches)

    assert nodes[0].name == 'NewStruct'
    assert nodes[1].name == 'NewEnum'

def test_rename_field():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('rename', ['field2', 'field69'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MyStruct', [model.StructMember('field1', 'u32'),
                                      model.StructMember('field69', 'u32'),
                                      model.StructMember('field3', 'u32')])] == nodes

def test_rename_field_not_composite():
    nodes = [model.Enum("MyEnum", [model.EnumMember("val", "123")])]

    patches = {'MyEnum': [patch.Action('rename', ['field3', 'field69'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Can rename fields only in composites: MyEnum' in str(e.value)

def test_rename_field_member_not_found():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]

    patches = {'MyStruct': [patch.Action('rename', ['unknown1', 'unknown2'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in str(e.value)

def test_rename_field_excessive_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]

    patches = {'MyStruct': [patch.Action('rename', 3 * ['too_much_params'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Rename must have 1 or 2 params: MyStruct' in str(e.value)
