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
        ]),
        model.Struct('BuiltinFixed', [
            model.StructMember('x', 'u32', size = 2)
        ]),
        model.Struct('BuiltinDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u32', bound = 'num_of_x')
        ]),
        model.Struct('BuiltinLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u32', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('BuiltinGreedy', [
            model.StructMember('x', 'u32', unlimited = True)
        ])
    ])

@pytest.fixture
def Fixcomp():
    return process([
        model.Struct('Fixcomp', [
            model.StructMember('x', 'Fixcomp'),
            model.StructMember('y', 'Fixcomp')
        ]),
        model.Struct('FixcompFixed', [
            model.StructMember('x', 'Fixcomp', size = 2)
        ]),
        model.Struct('FixcompDynamic', [
            model.StructMember('num_of_x', 'Fixcomp'),
            model.StructMember('x', 'Fixcomp', bound = 'num_of_x')
        ]),
        model.Struct('FixcompLimited', [
            model.StructMember('num_of_x', 'Fixcomp'),
            model.StructMember('x', 'Fixcomp', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('FixcompGreedy', [
            model.StructMember('x', 'Fixcomp', unlimited = True)
        ])
    ])

def test_generate_builtin_encode(Builtin):
    assert generate_struct_encode(Builtin[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Builtin[1]) == """\
pos = do_encode<E>(pos, x.x, 2);
"""
    assert generate_struct_encode(Builtin[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""
    assert generate_struct_encode(Builtin[3]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), std::min(x.x.size(), size_t(2)));
pos = pos + 8;
"""
    assert generate_struct_encode(Builtin[4]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_fixcomp_encode(Fixcomp):
    assert generate_struct_encode(Fixcomp[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Fixcomp[1]) == """\
pos = do_encode<E>(pos, x.x, 2);
"""
    assert generate_struct_encode(Fixcomp[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""
    assert generate_struct_encode(Fixcomp[3]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), std::min(x.x.size(), size_t(2)));
pos = pos + 16;
"""
    assert generate_struct_encode(Fixcomp[4]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""
