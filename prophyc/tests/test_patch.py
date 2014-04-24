import tempfile
import pytest

import patch
import model

def parse(content):
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(content)
        temp.flush()
        return patch.parse(temp.name)

def test_parsing():
    content = """\
MyStruct change_field_type lastField MyRealMember
YourStruct change_field_type firstField YourRealMember
"""

    patches = parse(content)

    assert {'MyStruct': ('change_field_type', ['lastField', 'MyRealMember']),
            'YourStruct': ('change_field_type', ['firstField', 'YourRealMember'])} == patches

def test_unknown_action():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': patch.Action('typo_or_something', [])}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Unknown action: MyStruct Action(action='typo_or_something', params=[])" == e.value.message

def test_change_field_type():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': patch.Action('change_field_type', ['field2', 'TheRealType'])}

    patch.patch(nodes, patches)

    assert [('MyStruct', [('field1', 'u32', None, None, None, None),
                          ('field2', 'TheRealType', None, None, None, None),
                          ('field3', 'u32', None, None, None, None)])] == nodes

def test_change_field_type_not_a_struct():
    nodes = [model.Typedef("MyStruct", "MyRealStruct")]
    patches = {'MyStruct': patch.Action('change_field_type', ['field2', 'TheRealType'])}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert "Can change field only in struct: MyStruct Action(action='change_field_type', params=['field2', 'TheRealType'])" == e.value.message

def test_change_field_type_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]

    patches = {'MyStruct': patch.Action('change_field_type', ['field2'])}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

    patches = {'MyStruct': patch.Action('change_field_type', ['field2', 'TheRealType', 'extra'])}
    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Change field must have 2 params: MyStruct' in e.value.message

def test_change_field_type_no_2_params():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': patch.Action('change_field_type', ['field4', 'TheRealType'])}

    with pytest.raises(Exception) as e:
        patch.patch(nodes, patches)
    assert 'Member not found: MyStruct' in e.value.message

def test_make_field_dynamic_array():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': patch.Action('make_field_dynamic_array', ['field3', 'field1'])}

    patch.patch(nodes, patches)

    assert [('MyStruct', [('field1', 'u32', None, None, None, None),
                          ('field2', 'u32', None, None, None, None),
                          ('field3', 'u32', True, 'field1', None, None)])] == nodes
