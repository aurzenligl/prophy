import tempfile
import pytest

import patch
import model

def parse(content):
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(content)
        temp.flush()
        return patch.parse(temp.name)

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
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('typo_or_something', [])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Unknown action: MyStruct Action(action='typo_or_something', params=[])" == e.value.message

def test_change_field_type():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('type', ['field2', 'TheRealType'])]}

    patch.patch(nodes, patches)

    assert [('MyStruct', [('field1', 'u32', None, None, None, None),
                          ('field2', 'TheRealType', None, None, None, None),
                          ('field3', 'u32', None, None, None, None)])] == nodes

def test_change_field_type_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('type', ['field2', 'TheRealType'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct Action(action='type', params=['field2', 'TheRealType'])" == e.value.message

def test_change_field_type_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]

    patches = {'MyStruct': [patch.Action('type', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

    patches = {'MyStruct': [patch.Action('type', ['field2', 'TheRealType', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

def test_change_field_type_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('type', ['field4', 'TheRealType'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message


def test_insert_field():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8']),
                            patch.Action('insert', ['-1', 'additional2', 'u16']),
                            patch.Action('insert', ['128', 'additional3', 'u64'])]}

    patch.patch(nodes, patches)

    assert [('MyStruct', [('field1', 'u32', None, None, None, None),
                          ('additional1', 'u8', None, None, None, None),
                          ('field2', 'u32', None, None, None, None),
                          ('additional2', 'u16', None, None, None, None),
                          ('field3', 'u32', None, None, None, None),
                          ('additional3', 'u64', None, None, None, None)])] == nodes

def test_insert_field_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Can insert field only in struct: MyStruct' in e.value.message

def test_insert_field_no_3_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('insert', ['1', 'additional1', 'u8', 'extra'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 3 params: MyStruct' in e.value.message

def test_insert_field_index_not_an_int():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('insert', ['not_a_number', 'additional1', 'u8'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Index is not a number: MyStruct' in e.value.message

def test_remove_field():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('remove', ['field2'])]}

    patch.patch(nodes, patches)

    assert [('MyStruct', [('field1', 'u32', None, None, None, None),
                          ('field3', 'u32', None, None, None, None)])] == nodes

def test_remove_field_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('remove', ['field2'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Can remove field only in struct: MyStruct' in e.value.message

def test_remove_field_no_1_param():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('remove', ['field1', 'extra_param'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Remove field must have 1 param: MyStruct' in e.value.message

def test_remove_field_not_found():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('remove', ['not_a_field'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message

def test_make_field_dynamic_array():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('dynamic', ['field3', 'field1'])]}

    patch.patch(nodes, patches)

    assert [('MyStruct', [('field1', 'u32', None, None, None, None),
                          ('field2', 'u32', None, None, None, None),
                          ('field3', 'u32', True, 'field1', None, None)])] == nodes

def test_make_field_dynamic_array_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': [patch.Action('dynamic', ['field2', 'field1'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct" in e.value.message

def test_make_field_dynamic_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]

    patches = {'MyStruct': [patch.Action('dynamic', ['field2'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

    patches = {'MyStruct': [patch.Action('dynamic', ['field2', 'field1', 'extra'])]}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

def test_make_field_dynamic_array_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': [patch.Action('dynamic', ['field4', 'field1'])]}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message
