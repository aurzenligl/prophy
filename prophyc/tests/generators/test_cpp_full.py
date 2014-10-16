import pytest
from prophyc import model
from prophyc.generators.cpp_full import generate_struct_encode

def process(nodes):
    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    model.evaluate_sizes(nodes)
    return nodes

@pytest.fixture
def Builtin():
    return process([
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ])
    ])

def test_generate_builtin_encode(Builtin):
    assert generate_struct_encode(Builtin[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
