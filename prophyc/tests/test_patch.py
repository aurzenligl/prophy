import os
import tempfile
import pytest

from prophyc import patch
from prophyc import model
from util import *

def parse(content):
    try:
        with tempfile.NamedTemporaryFile(delete = False) as temp:
            temp.write(content)
            temp.flush()
            return patch.parse(temp.name)
    finally:
        os.unlink(temp.name)

def test_parsing_ignoring_empty_lines():
    content = """\

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
    assert "Unknown action: MyStruct Action(action='typo_or_something', params=[])" == e.value.message

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
    assert "Can change field only in struct: MyStruct Action(action='type', params=['field2', 'TheRealType'])" == e.value.message

def test_change_field_type_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('type', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

    patches = {'MyStruct': [patch.Action('type', ['field2', 'TheRealType', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

def test_change_field_type_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('type', ['field4', 'TheRealType'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message


def test_insert_field():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8']),
                            patch.Action('insert', ['-1', 'additional2', 'u16']),
                            patch.Action('insert', ['128', 'additional3', 'u64'])]}

    patch.patch(nodes, patches)

    assert [model.Struct('MySdtruct', [model.StructMember('field1', 'u32'),
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
    assert 'Can insert field only in struct: MyStruct' in e.value.message

def test_insert_field_no_3_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8', 'extra'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 3 params: MyStruct' in e.value.message

def test_insert_field_index_not_an_int():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('insert', ['not_a_number', 'additional1', 'u8'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Index is not a number: MyStruct' in e.value.message

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
    assert 'Can remove field only in struct: MyStruct' in e.value.message

def test_remove_field_no_1_param():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('remove', ['field1', 'extra_param'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Remove field must have 1 param: MyStruct' in e.value.message

def test_remove_field_not_found():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32")])]
    patches = {'MyStruct': [patch.Action('remove', ['not_a_field'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message

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
    assert "Can change field only in struct: MyStruct" in e.value.message

def test_make_field_dynamic_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('dynamic', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

    patches = {'MyStruct': [patch.Action('dynamic', ['field2', 'field1', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

def test_make_field_dynamic_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('dynamic', ['field4', 'field1'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message

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
    assert "Can change field only in struct: MyStruct" in e.value.message

def test_make_field_greedy_array_no_1_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('greedy', ['field2', 'extra_args'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 1 params: MyStruct' in e.value.message


def test_make_field_greedy_array_with_wrong_name_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('greedy', ['field4'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message

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
    assert "Can change field only in struct: MyStruct" in e.value.message

def test_make_field_static_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('static', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

    patches = {'MyStruct': [patch.Action('static', ['field2', '3', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

def test_make_field_static_array_with_wrong_name_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('static', ['field4', '3'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message

def test_make_field_static_array_with_wrong_size_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('static', ['field3', 'wrong_size'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Size is not a number: MyStruct' in e.value.message

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
    assert "Can change field only in struct: MyStruct" in e.value.message

def test_make_field_limited_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]

    patches = {'MyStruct': [patch.Action('limited', ['field3'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

    patches = {'MyStruct': [patch.Action('limited', ['field3', 'field2', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

def test_make_field_limited_array_with_wrong_name_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('limited', ['field4', 'field2'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message

def test_make_field_limited_array_with_wrong_bound_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32"),
                                       model.StructMember("field2", "u32"),
                                       model.StructMember("field3", "u32")])]
    patches = {'MyStruct': [patch.Action('limited', ['field3', 'field4'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Array len member not found: MyStruct' in e.value.message
