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
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('Fixcomp', [
            model.StructMember('x', 'Builtin'),
            model.StructMember('y', 'Builtin')
        ]),
        model.Struct('FixcompFixed', [
            model.StructMember('x', 'Builtin', size = 2)
        ]),
        model.Struct('FixcompDynamic', [
            model.StructMember('num_of_x', 'Builtin'),
            model.StructMember('x', 'Builtin', bound = 'num_of_x')
        ]),
        model.Struct('FixcompLimited', [
            model.StructMember('num_of_x', 'Builtin'),
            model.StructMember('x', 'Builtin', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('FixcompGreedy', [
            model.StructMember('x', 'Builtin', unlimited = True)
        ])
    ])

@pytest.fixture
def Dyncomp():
    return process([
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('Dyncomp', [
            model.StructMember('x', 'Builtin'),
            model.StructMember('y', 'Builtin')
        ]),
        model.Struct('DyncompDynamic', [
            model.StructMember('num_of_x', 'Builtin'),
            model.StructMember('x', 'Builtin', bound = 'num_of_x')
        ]),
        model.Struct('DyncompGreedy', [
            model.StructMember('x', 'Builtin', unlimited = True)
        ])
    ])

@pytest.fixture
def Endpad():
    return process([
        model.Struct('Endpad', [
            model.StructMember('x', 'u16'),
            model.StructMember('y', 'u8')
        ]),
        model.Struct('EndpadFixed', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u8', size = 3)
        ]),
        model.Struct('EndpadDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x')
        ]),
        model.Struct('EndpadLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('EndpadGreedy', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u8', unlimited = True)
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
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Builtin[3]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 8;
"""
    assert generate_struct_encode(Builtin[4]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_fixcomp_encode(Fixcomp):
    assert generate_struct_encode(Fixcomp[1]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Fixcomp[2]) == """\
pos = do_encode<E>(pos, x.x, 2);
"""
    assert generate_struct_encode(Fixcomp[3]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Fixcomp[4]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 16;
"""
    assert generate_struct_encode(Fixcomp[5]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_dyncomp_encode(Dyncomp):
    assert generate_struct_encode(Dyncomp[1]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Dyncomp[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Dyncomp[3]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_endpad_encode(Endpad):
    assert generate_struct_encode(Endpad[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
pos = pos + 1;
"""
    assert generate_struct_encode(Endpad[1]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y, 3);
pos = pos + 1;
"""
    assert generate_struct_encode(Endpad[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<4>(pos);
"""
    assert generate_struct_encode(Endpad[3]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 2;
pos = pos + 2;
"""
    assert generate_struct_encode(Endpad[4]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y.data(), x.y.size());
pos = align<4>(pos);
"""
