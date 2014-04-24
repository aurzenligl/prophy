import tempfile
import patch

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
