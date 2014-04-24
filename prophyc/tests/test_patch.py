import tempfile
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

def test_change_field_type():
    nodes = [model.Struct("MyStruct", [model.StructMember("field1", "u32", None, None, None, None),
                                       model.StructMember("field2", "u32", None, None, None, None),
                                       model.StructMember("field3", "u32", None, None, None, None)])]
    patches = {'MyStruct': patch.Action('change_field_type', ['field2', 'TheRealType'])}

    patch.patch(nodes, patches)

    assert [('MyStruct', [('field1', 'u32', None, None, None, None),
                          ('field2', 'TheRealType', None, None, None, None),
                          ('field3', 'u32', None, None, None, None)])] == nodes
