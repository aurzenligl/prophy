import pytest
from prophyc import model
from prophyc.generators.cpp_full import (
    generate_include_definition,
    generate_constant_definition,
    generate_typedef_definition,
    generate_enum_definition,
    generate_enum_implementation,
    generate_struct_definition,
    generate_struct_implementation,
    generate_struct_encode,
    generate_struct_decode,
    generate_struct_print,
    generate_struct_encoded_byte_size,
    generate_struct_get_byte_size,
    generate_struct_fields,
    generate_struct_constructor,
    generate_union_definition,
    generate_union_implementation,
    generate_union_encode,
    generate_union_decode,
    generate_union_print,
    generate_union_encoded_byte_size,
    generate_union_get_byte_size,
    generate_union_fields,
    generate_union_constructor,
    generate_hpp_content,
    generate_hpp,
    generate_cpp,
    GenerateError,
    CppFullGenerator
)

def process(nodes):
    model.cross_reference(nodes)
    model.evaluate_kinds(nodes)
    model.evaluate_sizes(nodes)
    return nodes

@pytest.fixture(scope = 'session')
def Include():
    return process([
        model.Include('Arrays', [])
    ])

@pytest.fixture(scope = 'session')
def Constant():
    return process([
        model.Constant('CONSTANT', '3'),
        model.Constant('CONSTANT_WITH_IDENTIFIER', 'xyz')
    ])

@pytest.fixture(scope = 'session')
def Enum():
    return process([
        model.Enum('Enum', [
            model.EnumMember('Enum_One', '1'),
            model.EnumMember('Enum_Two', '0x2'),
            model.EnumMember('Enum_Three', '0o3'),
            model.EnumMember('Enum_Four', '-4')
        ])
    ])

@pytest.fixture(scope = 'session')
def Typedef():
    return process([
        model.Typedef('TU16', 'u16'),
        model.Typedef('TX', 'X')
    ])

@pytest.fixture(scope = 'session')
def Struct():
    return process([
        model.Struct('X', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('Y', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'X', bound = 'num_of_x')
        ])
    ])

@pytest.fixture(scope = 'session')
def Union():
    return process([
        model.Union('X', [
            model.UnionMember('a', 'u8', '1')
        ])
    ])

def test_generate_include_definition(Include):
    assert generate_include_definition(Include[0]) == """\
#include "Arrays.ppf.hpp"
"""

def test_generate_constant_definition(Constant):
    assert generate_constant_definition(Constant[0]) == """\
enum { CONSTANT = 3u };
"""
    assert generate_constant_definition(Constant[1]) == """\
enum { CONSTANT_WITH_IDENTIFIER = xyz };
"""

def test_generate_enum_definition(Enum):
    assert generate_enum_definition(Enum[0]) == """\
enum Enum
{
    Enum_One = 1u,
    Enum_Two = 0x2u,
    Enum_Three = 0o3u,
    Enum_Four = -4
};
"""

def test_generate_typedef_definition(Typedef):
    assert generate_typedef_definition(Typedef[0]) == """\
typedef uint16_t TU16;
"""
    assert generate_typedef_definition(Typedef[1]) == """\
typedef X TX;
"""

def test_generate_struct_definition(Struct):
    assert generate_struct_definition(Struct[0]) == """\
struct X : public prophy::detail::message<X>
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint32_t y;

    X(): x(), y() { }
    X(uint32_t _1, uint32_t _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};
"""
    assert generate_struct_definition(Struct[1]) == """\
struct Y : public prophy::detail::message<Y>
{
    enum { encoded_byte_size = -1 };

    std::vector<X> x;

    Y() { }
    Y(const std::vector<X>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return x.size() * 8 + 4;
    }
};
"""

def test_generate_union_definition(Union):
    assert generate_union_definition(Union[0]) == """\
struct X : public prophy::detail::message<X>
{
    enum { encoded_byte_size = 8 };

    enum _discriminator
    {
        discriminator_a = 1
    } discriminator;

    static const prophy::detail::int2type<discriminator_a> discriminator_a_t;

    uint8_t a;

    X(): discriminator(discriminator_a), a() { }
    X(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};
"""

def test_generate_enum_implementation(Enum):
    assert generate_enum_implementation(Enum[0]) == """\
template <>
const char* print_traits<Enum>::to_literal(Enum x)
{
    switch (x)
    {
        case Enum_One: return "Enum_One";
        case Enum_Two: return "Enum_Two";
        case Enum_Three: return "Enum_Three";
        case Enum_Four: return "Enum_Four";
        default: return 0;
    }
}
"""

def test_generate_struct_implementation(Struct):
    assert generate_struct_implementation(Struct[0]) == """\
template <>
template <endianness E>
uint8_t* message_impl<X>::encode(const X& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<X>::encode<native>(const X& x, uint8_t* pos);
template uint8_t* message_impl<X>::encode<little>(const X& x, uint8_t* pos);
template uint8_t* message_impl<X>::encode<big>(const X& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<X>::decode(X& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<X>::decode<native>(X& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<X>::decode<little>(X& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<X>::decode<big>(X& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<X>::print(const X& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "x", x.x);
    do_print(out, indent, "y", x.y);
}
template void message_impl<X>::print(const X& x, std::ostream& out, size_t indent);
"""
    assert generate_struct_implementation(Struct[1]) == """\
template <>
template <endianness E>
uint8_t* message_impl<Y>::encode(const Y& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
    return pos;
}
template uint8_t* message_impl<Y>::encode<native>(const Y& x, uint8_t* pos);
template uint8_t* message_impl<Y>::encode<little>(const Y& x, uint8_t* pos);
template uint8_t* message_impl<Y>::encode<big>(const Y& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Y>::decode(Y& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end)
    );
}
template bool message_impl<Y>::decode<native>(Y& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Y>::decode<little>(Y& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Y>::decode<big>(Y& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Y>::print(const Y& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "x", x.x.data(), x.x.size());
}
template void message_impl<Y>::print(const Y& x, std::ostream& out, size_t indent);
"""

def test_generate_union_implementation(Union):
    assert generate_union_implementation(Union[0]) == """\
template <>
template <endianness E>
uint8_t* message_impl<X>::encode(const X& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.discriminator);
    switch (x.discriminator)
    {
        case X::discriminator_a: do_encode<E>(pos, x.a); break;
    }
    pos = pos + 4;
    return pos;
}
template uint8_t* message_impl<X>::encode<native>(const X& x, uint8_t* pos);
template uint8_t* message_impl<X>::encode<little>(const X& x, uint8_t* pos);
template uint8_t* message_impl<X>::encode<big>(const X& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<X>::decode(X& x, const uint8_t*& pos, const uint8_t* end)
{
    if (!do_decode<E>(x.discriminator, pos, end)) return false;
    switch (x.discriminator)
    {
        case X::discriminator_a: if (!do_decode_in_place<E>(x.a, pos, end)) return false; break;
        default: return false;
    }
    return do_decode_advance(4, pos, end);
}
template bool message_impl<X>::decode<native>(X& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<X>::decode<little>(X& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<X>::decode<big>(X& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<X>::print(const X& x, std::ostream& out, size_t indent)
{
    switch (x.discriminator)
    {
        case X::discriminator_a: do_print(out, indent, "a", x.a); break;
    }
}
template void message_impl<X>::print(const X& x, std::ostream& out, size_t indent);
"""

@pytest.fixture(scope = 'session')
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

@pytest.fixture(scope = 'session')
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
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'Builtin', bound = 'num_of_x')
        ]),
        model.Struct('FixcompLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'Builtin', size = 2, bound = 'num_of_x')
        ]),
        model.Struct('FixcompGreedy', [
            model.StructMember('x', 'Builtin', unlimited = True)
        ])
    ])

@pytest.fixture(scope = 'session')
def Dyncomp():
    return process([
        model.Struct('BuiltinDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u32', bound = 'num_of_x')
        ]),
        model.Struct('Dyncomp', [
            model.StructMember('x', 'BuiltinDynamic')
        ]),
        model.Struct('DyncompDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'BuiltinDynamic', bound = 'num_of_x')
        ]),
        model.Struct('DyncompGreedy', [
            model.StructMember('x', 'BuiltinDynamic', unlimited = True)
        ])
    ])

@pytest.fixture(scope = 'session')
def Unions():
    return process([
        model.Struct('Builtin', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u32')
        ]),
        model.Union('Union', [
            model.UnionMember('a', 'u8', '1'),
            model.UnionMember('b', 'u32', '2'),
            model.UnionMember('c', 'Builtin', '3')
        ]),
        model.Struct('BuiltinOptional', [
            model.StructMember('x', 'u32', optional = True)
        ]),
        model.Struct('FixcompOptional', [
            model.StructMember('x', 'Builtin', optional = True)
        ])
    ])

@pytest.fixture(scope = 'session')
def Enums():
    return process([
        model.Enum('Enum', [
            model.EnumMember('Enum_One', '1'),
            model.EnumMember('Enum_Two', '2')
        ]),
        model.Struct('DynEnum', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'Enum', bound = 'num_of_x')
        ]),
        model.Constant('CONSTANT', '3'),
        model.Typedef('TU16', 'u16'),
        model.Struct('ConstantTypedefEnum', [
            model.StructMember('a', 'u16', size = 'CONSTANT'),
            model.StructMember('b', 'TU16'),
            model.StructMember('c', 'Enum')
        ])
    ])

@pytest.fixture(scope = 'session')
def Floats():
    return process([
        model.Struct('Floats', [
            model.StructMember('a', 'r32'),
            model.StructMember('b', 'r64')
        ])
    ])

@pytest.fixture(scope = 'session')
def Bytes():
    return process([
        model.Struct('BytesFixed', [
            model.StructMember('x', 'byte', size = 3)
        ]),
        model.Struct('BytesDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'byte', bound = 'num_of_x')
        ]),
        model.Struct('BytesLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'byte', size = 4, bound = 'num_of_x')
        ]),
        model.Struct('BytesGreedy', [
            model.StructMember('x', 'byte', unlimited = True)
        ])
    ])

@pytest.fixture(scope = 'session')
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

@pytest.fixture(scope = 'session')
def Scalarpad():
    return process([
        model.Struct('Scalarpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'u16')
        ]),
        model.Struct('ScalarpadComppre_Helper', [
            model.StructMember('x', 'u8')
        ]),
        model.Struct('ScalarpadComppre', [
            model.StructMember('x', 'ScalarpadComppre_Helper'),
            model.StructMember('y', 'u16')
        ]),
        model.Struct('ScalarpadComppost_Helper', [
            model.StructMember('x', 'u16')
        ]),
        model.Struct('ScalarpadComppost', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'ScalarpadComppost_Helper')
        ]),
    ])

@pytest.fixture(scope = 'session')
def Unionpad():
    return process([
        model.Struct('UnionpadOptionalboolpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'u8', optional = True)
        ]),
        model.Struct('UnionpadOptionalvaluepad', [
            model.StructMember('x', 'u64', optional = True)
        ]),
        model.Union('UnionpadDiscpad_Helper', [
            model.UnionMember('a', 'u8', '1')
        ]),
        model.Struct('UnionpadDiscpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'UnionpadDiscpad_Helper')
        ]),
        model.Union('UnionpadArmpad_Helper', [
            model.UnionMember('a', 'u8', '1'),
            model.UnionMember('b', 'u64', '2')
        ]),
        model.Struct('UnionpadArmpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'UnionpadArmpad_Helper')
        ])
    ])

@pytest.fixture(scope = 'session')
def Arraypad():
    return process([
        model.Struct('ArraypadCounter', [
            model.StructMember('num_of_x', 'u8'),
            model.StructMember('x', 'u16', bound = 'num_of_x')
        ]),
        model.Struct('ArraypadCounterSeparated', [
            model.StructMember('num_of_x', 'u8'),
            model.StructMember('y', 'u32'),
            model.StructMember('x', 'u32', bound = 'num_of_x')
        ]),
        model.Struct('ArraypadCounterAligns_Helper', [
            model.StructMember('num_of_x', 'u16'),
            model.StructMember('x', 'u8', bound = 'num_of_x')
        ]),
        model.Struct('ArraypadCounterAligns', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'ArraypadCounterAligns_Helper')
        ]),
        model.Struct('ArraypadFixed', [
            model.StructMember('x', 'u32'),
            model.StructMember('y', 'u8', size = 3),
            model.StructMember('z', 'u32')
        ]),
        model.Struct('ArraypadDynamic', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
            model.StructMember('y', 'u32')
        ]),
        model.Struct('ArraypadLimited', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', size = 2, bound = 'num_of_x'),
            model.StructMember('y', 'u32')
        ])
    ])

@pytest.fixture(scope = 'session')
def Dynfields():
    return process([
        model.Struct('Dynfields', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
            model.StructMember('num_of_y', 'u16'),
            model.StructMember('y', 'u16', bound = 'num_of_y'),
            model.StructMember('z', 'u64')
        ]),
        model.Struct('DynfieldsMixed', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('num_of_y', 'u16'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
            model.StructMember('y', 'u16', bound = 'num_of_y')
        ]),
        model.Struct('DynfieldsOverlapped', [
            model.StructMember('num_of_a', 'u32'),
            model.StructMember('num_of_b', 'u32'),
            model.StructMember('b', 'u16', bound = 'num_of_b'),
            model.StructMember('num_of_c', 'u32'),
            model.StructMember('c', 'u16', bound = 'num_of_c'),
            model.StructMember('a', 'u16', bound = 'num_of_a')
        ]),
        model.Struct('DynfieldsPartialpad_Helper', [
            model.StructMember('num_of_x', 'u8'),
            model.StructMember('x', 'u8', bound = 'num_of_x'),
            model.StructMember('y', 'u8'),
            model.StructMember('z', 'u64')
        ]),
        model.Struct('DynfieldsPartialpad', [
            model.StructMember('x', 'u8'),
            model.StructMember('y', 'DynfieldsPartialpad_Helper')
        ]),
        model.Struct('DynfieldsScalarpartialpad_Helper', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'u8', bound = 'num_of_x')
        ]),
        model.Struct('DynfieldsScalarpartialpad', [
            model.StructMember('x', 'DynfieldsScalarpartialpad_Helper'),
            model.StructMember('y', 'DynfieldsScalarpartialpad_Helper'),
            model.StructMember('z', 'DynfieldsScalarpartialpad_Helper')
        ])
    ])

def test_generate_builtin_encode(Builtin):
    assert generate_struct_encode(Builtin[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Builtin[1]) == """\
pos = do_encode<E>(pos, x.x.data(), 2);
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
pos = do_encode<E>(pos, x.x.data(), 2);
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
"""
    assert generate_struct_encode(Dyncomp[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Dyncomp[3]) == """\
pos = do_encode<E>(pos, x.x.data(), x.x.size());
"""

def test_generate_unions_encode(Unions):
    assert generate_union_encode(Unions[1]) == """\
pos = do_encode<E>(pos, x.discriminator);
switch (x.discriminator)
{
    case Union::discriminator_a: do_encode<E>(pos, x.a); break;
    case Union::discriminator_b: do_encode<E>(pos, x.b); break;
    case Union::discriminator_c: do_encode<E>(pos, x.c); break;
}
pos = pos + 8;
"""
    assert generate_struct_encode(Unions[2]) == """\
pos = do_encode<E>(pos, x.x);
"""
    assert generate_struct_encode(Unions[3]) == """\
pos = do_encode<E>(pos, x.x);
"""

def test_generate_enums_encode(Enums):
    assert generate_struct_encode(Enums[1]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
"""
    assert generate_struct_encode(Enums[4]) == """\
pos = do_encode<E>(pos, x.a.data(), CONSTANT);
pos = do_encode<E>(pos, x.b);
pos = do_encode<E>(pos, x.c);
"""

def test_generate_floats_encode(Floats):
    assert generate_struct_encode(Floats[0]) == """\
pos = do_encode<E>(pos, x.a);
pos = pos + 4;
pos = do_encode<E>(pos, x.b);
"""

def test_generate_bytes_encode(Bytes):
    assert generate_struct_encode(Bytes[0]) == """\
pos = do_encode<E>(pos, x.x.data(), 3);
"""
    assert generate_struct_encode(Bytes[1]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<4>(pos);
"""
    assert generate_struct_encode(Bytes[2]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(4))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(4))));
pos = pos + 4;
"""
    assert generate_struct_encode(Bytes[3]) == """\
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
pos = do_encode<E>(pos, x.y.data(), 3);
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

def test_generate_scalarpad_encode(Scalarpad):
    assert generate_struct_encode(Scalarpad[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Scalarpad[2]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Scalarpad[4]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""

def test_generate_unionpad_encode(Unionpad):
    assert generate_struct_encode(Unionpad[0]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 3;
pos = do_encode<E>(pos, x.y);
pos = pos + 3;
"""
    assert generate_struct_encode(Unionpad[1]) == """\
pos = do_encode<E>(pos, x.x);
"""
    assert generate_union_encode(Unionpad[2]) == """\
pos = do_encode<E>(pos, x.discriminator);
switch (x.discriminator)
{
    case UnionpadDiscpad_Helper::discriminator_a: do_encode<E>(pos, x.a); break;
}
pos = pos + 4;
"""
    assert generate_struct_encode(Unionpad[3]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 3;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_union_encode(Unionpad[4]) == """\
pos = do_encode<E>(pos, x.discriminator);
pos = pos + 4;
switch (x.discriminator)
{
    case UnionpadArmpad_Helper::discriminator_a: do_encode<E>(pos, x.a); break;
    case UnionpadArmpad_Helper::discriminator_b: do_encode<E>(pos, x.b); break;
}
pos = pos + 8;
"""
    assert generate_struct_encode(Unionpad[5]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 7;
pos = do_encode<E>(pos, x.y);
"""

def test_generate_arraypad_encode(Arraypad):
    assert generate_struct_encode(Arraypad[0]) == """\
pos = do_encode<E>(pos, uint8_t(x.x.size()));
pos = pos + 1;
pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
"""
    assert generate_struct_encode(Arraypad[1]) == """\
pos = do_encode<E>(pos, uint8_t(x.x.size()));
pos = pos + 3;
pos = do_encode<E>(pos, x.y);
pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
"""
    assert generate_struct_encode(Arraypad[2]) == """\
pos = do_encode<E>(pos, uint16_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint16_t(x.x.size()));
pos = align<2>(pos);
"""
    assert generate_struct_encode(Arraypad[3]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 1;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Arraypad[4]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y.data(), 3);
pos = pos + 1;
pos = do_encode<E>(pos, x.z);
"""
    assert generate_struct_encode(Arraypad[5]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<4>(pos);
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Arraypad[6]) == """\
pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
do_encode<E>(pos, x.x.data(), uint32_t(std::min(x.x.size(), size_t(2))));
pos = pos + 2;
pos = pos + 2;
pos = do_encode<E>(pos, x.y);
"""

def test_generate_dynfields_encode(Dynfields):
    assert generate_struct_encode(Dynfields[0]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<2>(pos);
pos = do_encode<E>(pos, uint16_t(x.y.size()));
pos = do_encode<E>(pos, x.y.data(), uint16_t(x.y.size()));
pos = align<8>(pos);
pos = do_encode<E>(pos, x.z);
"""
    assert generate_struct_encode(Dynfields[1]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, uint16_t(x.y.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<2>(pos);
pos = do_encode<E>(pos, x.y.data(), uint16_t(x.y.size()));
pos = align<4>(pos);
"""
    assert generate_struct_encode(Dynfields[2]) == """\
pos = do_encode<E>(pos, uint32_t(x.a.size()));
pos = do_encode<E>(pos, uint32_t(x.b.size()));
pos = do_encode<E>(pos, x.b.data(), uint32_t(x.b.size()));
pos = align<4>(pos);
pos = do_encode<E>(pos, uint32_t(x.c.size()));
pos = do_encode<E>(pos, x.c.data(), uint32_t(x.c.size()));
pos = do_encode<E>(pos, x.a.data(), uint32_t(x.a.size()));
pos = align<4>(pos);
"""
    assert generate_struct_encode(Dynfields[3]) == """\
pos = do_encode<E>(pos, uint8_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
pos = align<8>(pos);
pos = do_encode<E>(pos, x.y);
pos = pos + 7;
pos = do_encode<E>(pos, x.z);
"""
    assert generate_struct_encode(Dynfields[4]) == """\
pos = do_encode<E>(pos, x.x);
pos = pos + 7;
pos = do_encode<E>(pos, x.y);
"""
    assert generate_struct_encode(Dynfields[5]) == """\
pos = do_encode<E>(pos, uint32_t(x.x.size()));
pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
pos = align<4>(pos);
"""
    assert generate_struct_encode(Dynfields[6]) == """\
pos = do_encode<E>(pos, x.x);
pos = do_encode<E>(pos, x.y);
pos = do_encode<E>(pos, x.z);
"""

def test_generate_builtin_decode(Builtin):
    assert generate_struct_decode(Builtin[0]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_struct_decode(Builtin[1]) == """\
do_decode<E>(x.x.data(), 2, pos, end)
"""
    assert generate_struct_decode(Builtin[2]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end)
"""
    assert generate_struct_decode(Builtin[3]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end, 2) &&
do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_advance(8, pos, end)
"""
    assert generate_struct_decode(Builtin[4]) == """\
do_decode_greedy<E>(x.x, pos, end)
"""

def test_generate_fixcomp_decode(Fixcomp):
    assert generate_struct_decode(Fixcomp[1]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_struct_decode(Fixcomp[2]) == """\
do_decode<E>(x.x.data(), 2, pos, end)
"""
    assert generate_struct_decode(Fixcomp[3]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end)
"""
    assert generate_struct_decode(Fixcomp[4]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end, 2) &&
do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_advance(16, pos, end)
"""
    assert generate_struct_decode(Fixcomp[5]) == """\
do_decode_greedy<E>(x.x, pos, end)
"""

def test_generate_dyncomp_decode(Dyncomp):
    assert generate_struct_decode(Dyncomp[1]) == """\
do_decode<E>(x.x, pos, end)
"""
    assert generate_struct_decode(Dyncomp[2]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end)
"""
    assert generate_struct_decode(Dyncomp[3]) == """\
do_decode_greedy<E>(x.x, pos, end)
"""

def test_generate_unions_decode(Unions):
    assert generate_union_decode(Unions[1]) == """\
if (!do_decode<E>(x.discriminator, pos, end)) return false;
switch (x.discriminator)
{
    case Union::discriminator_a: if (!do_decode_in_place<E>(x.a, pos, end)) return false; break;
    case Union::discriminator_b: if (!do_decode_in_place<E>(x.b, pos, end)) return false; break;
    case Union::discriminator_c: if (!do_decode_in_place<E>(x.c, pos, end)) return false; break;
    default: return false;
}
return do_decode_advance(8, pos, end);
"""
    assert generate_struct_decode(Unions[2]) == """\
do_decode<E>(x.x, pos, end)
"""
    assert generate_struct_decode(Unions[3]) == """\
do_decode<E>(x.x, pos, end)
"""

def test_generate_enums_decode(Enums):
    assert generate_struct_decode(Enums[1]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end)
"""
    assert generate_struct_decode(Enums[4]) == """\
do_decode<E>(x.a.data(), CONSTANT, pos, end) &&
do_decode<E>(x.b, pos, end) &&
do_decode<E>(x.c, pos, end)
"""

def test_generate_floats_decode(Floats):
    assert generate_struct_decode(Floats[0]) == """\
do_decode<E>(x.a, pos, end) &&
do_decode_advance(4, pos, end) &&
do_decode<E>(x.b, pos, end)
"""

def test_generate_bytes_decode(Bytes):
    assert generate_struct_decode(Bytes[0]) == """\
do_decode<E>(x.x.data(), 3, pos, end)
"""
    assert generate_struct_decode(Bytes[1]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<4>(pos, end)
"""
    assert generate_struct_decode(Bytes[2]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end, 4) &&
do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_advance(4, pos, end)
"""
    assert generate_struct_decode(Bytes[3]) == """\
do_decode_greedy<E>(x.x, pos, end)
"""

def test_generate_endpad_decode(Endpad):
    assert generate_struct_decode(Endpad[0]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode<E>(x.y, pos, end) &&
do_decode_advance(1, pos, end)
"""
    assert generate_struct_decode(Endpad[1]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode<E>(x.y.data(), 3, pos, end) &&
do_decode_advance(1, pos, end)
"""
    assert generate_struct_decode(Endpad[2]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<4>(pos, end)
"""
    assert generate_struct_decode(Endpad[3]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end, 2) &&
do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_advance(2, pos, end) &&
do_decode_advance(2, pos, end)
"""
    assert generate_struct_decode(Endpad[4]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_greedy<E>(x.y, pos, end) &&
do_decode_align<4>(pos, end)
"""

def test_generate_scalarpad_decode(Scalarpad):
    assert generate_struct_decode(Scalarpad[0]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(1, pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_struct_decode(Scalarpad[2]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(1, pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_struct_decode(Scalarpad[4]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(1, pos, end) &&
do_decode<E>(x.y, pos, end)
"""

def test_generate_unionpad_decode(Unionpad):
    assert generate_struct_decode(Unionpad[0]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(3, pos, end) &&
do_decode<E>(x.y, pos, end) &&
do_decode_advance(3, pos, end)
"""
    assert generate_struct_decode(Unionpad[1]) == """\
do_decode<E>(x.x, pos, end)
"""
    assert generate_union_decode(Unionpad[2]) == """\
if (!do_decode<E>(x.discriminator, pos, end)) return false;
switch (x.discriminator)
{
    case UnionpadDiscpad_Helper::discriminator_a: if (!do_decode_in_place<E>(x.a, pos, end)) return false; break;
    default: return false;
}
return do_decode_advance(4, pos, end);
"""
    assert generate_struct_decode(Unionpad[3]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(3, pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_union_decode(Unionpad[4]) == """\
if (!do_decode<E>(x.discriminator, pos, end)) return false;
if (!do_decode_advance(4, pos, end)) return false;
switch (x.discriminator)
{
    case UnionpadArmpad_Helper::discriminator_a: if (!do_decode_in_place<E>(x.a, pos, end)) return false; break;
    case UnionpadArmpad_Helper::discriminator_b: if (!do_decode_in_place<E>(x.b, pos, end)) return false; break;
    default: return false;
}
return do_decode_advance(8, pos, end);
"""
    assert generate_struct_decode(Unionpad[5]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(7, pos, end) &&
do_decode<E>(x.y, pos, end)
"""

def test_generate_arraypad_decode(Arraypad):
    assert generate_struct_decode(Arraypad[0]) == """\
do_decode_resize<E, uint8_t>(x.x, pos, end) &&
do_decode_advance(1, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end)
"""
    assert generate_struct_decode(Arraypad[1]) == """\
do_decode_resize<E, uint8_t>(x.x, pos, end) &&
do_decode_advance(3, pos, end) &&
do_decode<E>(x.y, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end)
"""
    assert generate_struct_decode(Arraypad[2]) == """\
do_decode_resize<E, uint16_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<2>(pos, end)
"""
    assert generate_struct_decode(Arraypad[3]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(1, pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_struct_decode(Arraypad[4]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode<E>(x.y.data(), 3, pos, end) &&
do_decode_advance(1, pos, end) &&
do_decode<E>(x.z, pos, end)
"""
    assert generate_struct_decode(Arraypad[5]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<4>(pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_struct_decode(Arraypad[6]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end, 2) &&
do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_advance(2, pos, end) &&
do_decode_advance(2, pos, end) &&
do_decode<E>(x.y, pos, end)
"""

def test_generate_dynfields_decode(Dynfields):
    assert generate_struct_decode(Dynfields[0]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<2>(pos, end) &&
do_decode_resize<E, uint16_t>(x.y, pos, end) &&
do_decode<E>(x.y.data(), x.y.size(), pos, end) &&
do_decode_align<8>(pos, end) &&
do_decode<E>(x.z, pos, end)
"""
    assert generate_struct_decode(Dynfields[1]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode_resize<E, uint16_t>(x.y, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<2>(pos, end) &&
do_decode<E>(x.y.data(), x.y.size(), pos, end) &&
do_decode_align<4>(pos, end)
"""
    assert generate_struct_decode(Dynfields[2]) == """\
do_decode_resize<E, uint32_t>(x.a, pos, end) &&
do_decode_resize<E, uint32_t>(x.b, pos, end) &&
do_decode<E>(x.b.data(), x.b.size(), pos, end) &&
do_decode_align<4>(pos, end) &&
do_decode_resize<E, uint32_t>(x.c, pos, end) &&
do_decode<E>(x.c.data(), x.c.size(), pos, end) &&
do_decode<E>(x.a.data(), x.a.size(), pos, end) &&
do_decode_align<4>(pos, end)
"""
    assert generate_struct_decode(Dynfields[3]) == """\
do_decode_resize<E, uint8_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<8>(pos, end) &&
do_decode<E>(x.y, pos, end) &&
do_decode_advance(7, pos, end) &&
do_decode<E>(x.z, pos, end)
"""
    assert generate_struct_decode(Dynfields[4]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode_advance(7, pos, end) &&
do_decode<E>(x.y, pos, end)
"""
    assert generate_struct_decode(Dynfields[5]) == """\
do_decode_resize<E, uint32_t>(x.x, pos, end) &&
do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
do_decode_align<4>(pos, end)
"""
    assert generate_struct_decode(Dynfields[6]) == """\
do_decode<E>(x.x, pos, end) &&
do_decode<E>(x.y, pos, end) &&
do_decode<E>(x.z, pos, end)
"""

def test_generate_builtin_print(Builtin):
    assert generate_struct_print(Builtin[0]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Builtin[1]) == """\
do_print(out, indent, "x", x.x.data(), size_t(2));
"""
    assert generate_struct_print(Builtin[2]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Builtin[3]) == """\
do_print(out, indent, "x", x.x.data(), std::min(x.x.size(), size_t(2)));
"""
    assert generate_struct_print(Builtin[4]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""

def test_generate_fixcomp_print(Fixcomp):
    assert generate_struct_print(Fixcomp[1]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Fixcomp[2]) == """\
do_print(out, indent, "x", x.x.data(), size_t(2));
"""
    assert generate_struct_print(Fixcomp[3]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Fixcomp[4]) == """\
do_print(out, indent, "x", x.x.data(), std::min(x.x.size(), size_t(2)));
"""
    assert generate_struct_print(Fixcomp[5]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""

def test_generate_dyncomp_print(Dyncomp):
    assert generate_struct_print(Dyncomp[1]) == """\
do_print(out, indent, "x", x.x);
"""
    assert generate_struct_print(Dyncomp[2]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Dyncomp[3]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""

def test_generate_unions_print(Unions):
    assert generate_union_print(Unions[1]) == """\
switch (x.discriminator)
{
    case Union::discriminator_a: do_print(out, indent, "a", x.a); break;
    case Union::discriminator_b: do_print(out, indent, "b", x.b); break;
    case Union::discriminator_c: do_print(out, indent, "c", x.c); break;
}
"""
    assert generate_struct_print(Unions[2]) == """\
if (x.x) do_print(out, indent, "x", *x.x);
"""
    assert generate_struct_print(Unions[3]) == """\
if (x.x) do_print(out, indent, "x", *x.x);
"""

def test_generate_enums_print(Enums):
    assert generate_struct_print(Enums[1]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Enums[4]) == """\
do_print(out, indent, "a", x.a.data(), size_t(CONSTANT));
do_print(out, indent, "b", x.b);
do_print(out, indent, "c", x.c);
"""

def test_generate_floats_print(Floats):
    assert generate_struct_print(Floats[0]) == """\
do_print(out, indent, "a", x.a);
do_print(out, indent, "b", x.b);
"""

def test_generate_bytes_print(Bytes):
    assert generate_struct_print(Bytes[0]) == """\
do_print(out, indent, "x", std::make_pair(x.x.data(), size_t(3)));
"""
    assert generate_struct_print(Bytes[1]) == """\
do_print(out, indent, "x", std::make_pair(x.x.data(), x.x.size()));
"""
    assert generate_struct_print(Bytes[2]) == """\
do_print(out, indent, "x", std::make_pair(x.x.data(), std::min(x.x.size(), size_t(4))));
"""
    assert generate_struct_print(Bytes[3]) == """\
do_print(out, indent, "x", std::make_pair(x.x.data(), x.x.size()));
"""

def test_generate_endpad_print(Endpad):
    assert generate_struct_print(Endpad[0]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Endpad[1]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y.data(), size_t(3));
"""
    assert generate_struct_print(Endpad[2]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Endpad[3]) == """\
do_print(out, indent, "x", x.x.data(), std::min(x.x.size(), size_t(2)));
"""
    assert generate_struct_print(Endpad[4]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y.data(), x.y.size());
"""

def test_generate_scalarpad_print(Scalarpad):
    assert generate_struct_print(Scalarpad[0]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Scalarpad[2]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Scalarpad[4]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""

def test_generate_unionpad_print(Unionpad):
    assert generate_struct_print(Unionpad[0]) == """\
do_print(out, indent, "x", x.x);
if (x.y) do_print(out, indent, "y", *x.y);
"""
    assert generate_struct_print(Unionpad[1]) == """\
if (x.x) do_print(out, indent, "x", *x.x);
"""
    assert generate_union_print(Unionpad[2]) == """\
switch (x.discriminator)
{
    case UnionpadDiscpad_Helper::discriminator_a: do_print(out, indent, "a", x.a); break;
}
"""
    assert generate_struct_print(Unionpad[3]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_union_print(Unionpad[4]) == """\
switch (x.discriminator)
{
    case UnionpadArmpad_Helper::discriminator_a: do_print(out, indent, "a", x.a); break;
    case UnionpadArmpad_Helper::discriminator_b: do_print(out, indent, "b", x.b); break;
}
"""
    assert generate_struct_print(Unionpad[5]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""

def test_generate_arraypad_print(Arraypad):
    assert generate_struct_print(Arraypad[0]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Arraypad[1]) == """\
do_print(out, indent, "y", x.y);
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Arraypad[2]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Arraypad[3]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Arraypad[4]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y.data(), size_t(3));
do_print(out, indent, "z", x.z);
"""
    assert generate_struct_print(Arraypad[5]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Arraypad[6]) == """\
do_print(out, indent, "x", x.x.data(), std::min(x.x.size(), size_t(2)));
do_print(out, indent, "y", x.y);
"""

def test_generate_dynfields_print(Dynfields):
    assert generate_struct_print(Dynfields[0]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
do_print(out, indent, "y", x.y.data(), x.y.size());
do_print(out, indent, "z", x.z);
"""
    assert generate_struct_print(Dynfields[1]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
do_print(out, indent, "y", x.y.data(), x.y.size());
"""
    assert generate_struct_print(Dynfields[2]) == """\
do_print(out, indent, "b", x.b.data(), x.b.size());
do_print(out, indent, "c", x.c.data(), x.c.size());
do_print(out, indent, "a", x.a.data(), x.a.size());
"""
    assert generate_struct_print(Dynfields[3]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
do_print(out, indent, "y", x.y);
do_print(out, indent, "z", x.z);
"""
    assert generate_struct_print(Dynfields[4]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
"""
    assert generate_struct_print(Dynfields[5]) == """\
do_print(out, indent, "x", x.x.data(), x.x.size());
"""
    assert generate_struct_print(Dynfields[6]) == """\
do_print(out, indent, "x", x.x);
do_print(out, indent, "y", x.y);
do_print(out, indent, "z", x.z);
"""

def test_generate_builtin_encoded_byte_size(Builtin):
    assert generate_struct_encoded_byte_size(Builtin[0]) == '8'
    assert generate_struct_encoded_byte_size(Builtin[1]) == '8'
    assert generate_struct_encoded_byte_size(Builtin[2]) == '-1'
    assert generate_struct_encoded_byte_size(Builtin[3]) == '12'
    assert generate_struct_encoded_byte_size(Builtin[4]) == '-1'

def test_generate_fixcomp_encoded_byte_size(Fixcomp):
    assert generate_struct_encoded_byte_size(Fixcomp[1]) == '16'
    assert generate_struct_encoded_byte_size(Fixcomp[2]) == '16'
    assert generate_struct_encoded_byte_size(Fixcomp[3]) == '-1'
    assert generate_struct_encoded_byte_size(Fixcomp[4]) == '20'
    assert generate_struct_encoded_byte_size(Fixcomp[5]) == '-1'

def test_generate_dyncomp_encoded_byte_size(Dyncomp):
    assert generate_struct_encoded_byte_size(Dyncomp[1]) == '-1'
    assert generate_struct_encoded_byte_size(Dyncomp[2]) == '-1'
    assert generate_struct_encoded_byte_size(Dyncomp[3]) == '-1'

def test_generate_unions_encoded_byte_size(Unions):
    assert generate_union_encoded_byte_size(Unions[1]) == '12'
    assert generate_struct_encoded_byte_size(Unions[2]) == '8'
    assert generate_struct_encoded_byte_size(Unions[3]) == '12'

def test_generate_enums_encoded_byte_size(Enums):
    assert generate_struct_encoded_byte_size(Enums[1]) == '-1'
    assert generate_struct_encoded_byte_size(Enums[4]) == '12'

def test_generate_floats_encoded_byte_size(Floats):
    assert generate_struct_encoded_byte_size(Floats[0]) == '16'

def test_generate_bytes_encoded_byte_size(Bytes):
    assert generate_struct_encoded_byte_size(Bytes[0]) == '3'
    assert generate_struct_encoded_byte_size(Bytes[1]) == '-1'
    assert generate_struct_encoded_byte_size(Bytes[2]) == '8'
    assert generate_struct_encoded_byte_size(Bytes[3]) == '-1'

def test_generate_endpad_encoded_byte_size(Endpad):
    assert generate_struct_encoded_byte_size(Endpad[0]) == '4'
    assert generate_struct_encoded_byte_size(Endpad[1]) == '8'
    assert generate_struct_encoded_byte_size(Endpad[2]) == '-1'
    assert generate_struct_encoded_byte_size(Endpad[3]) == '8'
    assert generate_struct_encoded_byte_size(Endpad[4]) == '-1'

def test_generate_scalarpad_encoded_byte_size(Scalarpad):
    assert generate_struct_encoded_byte_size(Scalarpad[0]) == '4'
    assert generate_struct_encoded_byte_size(Scalarpad[2]) == '4'
    assert generate_struct_encoded_byte_size(Scalarpad[4]) == '4'

def test_generate_unionpad_encoded_byte_size(Unionpad):
    assert generate_struct_encoded_byte_size(Unionpad[0]) == '12'
    assert generate_struct_encoded_byte_size(Unionpad[1]) == '16'
    assert generate_union_encoded_byte_size(Unionpad[2]) == '8'
    assert generate_struct_encoded_byte_size(Unionpad[3]) == '12'
    assert generate_union_encoded_byte_size(Unionpad[4]) == '16'
    assert generate_struct_encoded_byte_size(Unionpad[5]) == '24'

def test_generate_arraypad_encoded_byte_size(Arraypad):
    assert generate_struct_encoded_byte_size(Arraypad[0]) == '-1'
    assert generate_struct_encoded_byte_size(Arraypad[1]) == '-1'
    assert generate_struct_encoded_byte_size(Arraypad[2]) == '-1'
    assert generate_struct_encoded_byte_size(Arraypad[3]) == '-1'
    assert generate_struct_encoded_byte_size(Arraypad[4]) == '12'
    assert generate_struct_encoded_byte_size(Arraypad[5]) == '-1'
    assert generate_struct_encoded_byte_size(Arraypad[6]) == '12'

def test_generate_dynfields_encoded_byte_size(Dynfields):
    assert generate_struct_encoded_byte_size(Dynfields[0]) == '-1'
    assert generate_struct_encoded_byte_size(Dynfields[1]) == '-1'
    assert generate_struct_encoded_byte_size(Dynfields[2]) == '-1'
    assert generate_struct_encoded_byte_size(Dynfields[3]) == '-1'
    assert generate_struct_encoded_byte_size(Dynfields[4]) == '-1'
    assert generate_struct_encoded_byte_size(Dynfields[5]) == '-1'
    assert generate_struct_encoded_byte_size(Dynfields[6]) == '-1'

def test_generate_builtin_get_byte_size(Builtin):
    assert generate_struct_get_byte_size(Builtin[0]) == """\
return 8;
"""
    assert generate_struct_get_byte_size(Builtin[1]) == """\
return 8;
"""
    assert generate_struct_get_byte_size(Builtin[2]) == """\
return x.size() * 4 + 4;
"""
    assert generate_struct_get_byte_size(Builtin[3]) == """\
return 12;
"""
    assert generate_struct_get_byte_size(Builtin[4]) == """\
return x.size() * 4;
"""

def test_generate_fixcomp_get_byte_size(Fixcomp):
    assert generate_struct_get_byte_size(Fixcomp[1]) == """\
return 16;
"""
    assert generate_struct_get_byte_size(Fixcomp[2]) == """\
return 16;
"""
    assert generate_struct_get_byte_size(Fixcomp[3]) == """\
return x.size() * 8 + 4;
"""
    assert generate_struct_get_byte_size(Fixcomp[4]) == """\
return 20;
"""
    assert generate_struct_get_byte_size(Fixcomp[5]) == """\
return x.size() * 8;
"""

def test_generate_dyncomp_get_byte_size(Dyncomp):
    assert generate_struct_get_byte_size(Dyncomp[1]) == """\
return x.get_byte_size();
"""
    assert generate_struct_get_byte_size(Dyncomp[2]) == """\
return std::accumulate(x.begin(), x.end(), size_t(), prophy::detail::byte_size()) + 4;
"""
    assert generate_struct_get_byte_size(Dyncomp[3]) == """\
return std::accumulate(x.begin(), x.end(), size_t(), prophy::detail::byte_size());
"""

def test_generate_unions_get_byte_size(Unions):
    assert generate_union_get_byte_size(Unions[1]) == """\
return 12;
"""
    assert generate_struct_get_byte_size(Unions[2]) == """\
return 8;
"""
    assert generate_struct_get_byte_size(Unions[3]) == """\
return 12;
"""

def test_generate_enums_get_byte_size(Enums):
    assert generate_struct_get_byte_size(Enums[1]) == """\
return x.size() * 4 + 4;
"""
    assert generate_struct_get_byte_size(Enums[4]) == """\
return 12;
"""

def test_generate_floats_get_byte_size(Floats):
    assert generate_struct_get_byte_size(Floats[0]) == """\
return 16;
"""

def test_generate_bytes_get_byte_size(Bytes):
    assert generate_struct_get_byte_size(Bytes[0]) == """\
return 3;
"""
    assert generate_struct_get_byte_size(Bytes[1]) == """\
return prophy::detail::nearest<4>(
    x.size() * 1 + 4
);
"""
    assert generate_struct_get_byte_size(Bytes[2]) == """\
return 8;
"""
    assert generate_struct_get_byte_size(Bytes[3]) == """\
return x.size() * 1;
"""

def test_generate_endpad_get_byte_size(Endpad):
    assert generate_struct_get_byte_size(Endpad[0]) == """\
return 4;
"""
    assert generate_struct_get_byte_size(Endpad[1]) == """\
return 8;
"""
    assert generate_struct_get_byte_size(Endpad[2]) == """\
return prophy::detail::nearest<4>(
    x.size() * 1 + 4
);
"""
    assert generate_struct_get_byte_size(Endpad[3]) == """\
return 8;
"""
    assert generate_struct_get_byte_size(Endpad[4]) == """\
return prophy::detail::nearest<4>(
    y.size() * 1 + 4
);
"""

def test_generate_scalarpad_get_byte_size(Scalarpad):
    assert generate_struct_get_byte_size(Scalarpad[0]) == """\
return 4;
"""
    assert generate_struct_get_byte_size(Scalarpad[2]) == """\
return 4;
"""
    assert generate_struct_get_byte_size(Scalarpad[4]) == """\
return 4;
"""

def test_generate_unionpad_get_byte_size(Unionpad):
    assert generate_struct_get_byte_size(Unionpad[0]) == """\
return 12;
"""
    assert generate_struct_get_byte_size(Unionpad[1]) == """\
return 16;
"""
    assert generate_union_get_byte_size(Unionpad[2]) == """\
return 8;
"""
    assert generate_struct_get_byte_size(Unionpad[3]) == """\
return 12;
"""
    assert generate_union_get_byte_size(Unionpad[4]) == """\
return 16;
"""
    assert generate_struct_get_byte_size(Unionpad[5]) == """\
return 24;
"""

def test_generate_arraypad_get_byte_size(Arraypad):
    assert generate_struct_get_byte_size(Arraypad[0]) == """\
return x.size() * 2 + 2;
"""
    assert generate_struct_get_byte_size(Arraypad[1]) == """\
return x.size() * 4 + 8;
"""
    assert generate_struct_get_byte_size(Arraypad[2]) == """\
return prophy::detail::nearest<2>(
    x.size() * 1 + 2
);
"""
    assert generate_struct_get_byte_size(Arraypad[3]) == """\
return y.get_byte_size() + 2;
"""
    assert generate_struct_get_byte_size(Arraypad[4]) == """\
return 12;
"""
    assert generate_struct_get_byte_size(Arraypad[5]) == """\
return prophy::detail::nearest<4>(
    x.size() * 1 + 4
) + 4;
"""
    assert generate_struct_get_byte_size(Arraypad[6]) == """\
return 12;
"""

def test_generate_dynfields_get_byte_size(Dynfields):
    assert generate_struct_get_byte_size(Dynfields[0]) == """\
return prophy::detail::nearest<8>(
    prophy::detail::nearest<2>(
        x.size() * 1 + 4
    ) + y.size() * 2 + 2
) + 8;
"""
    assert generate_struct_get_byte_size(Dynfields[1]) == """\
return prophy::detail::nearest<4>(
    prophy::detail::nearest<2>(
        x.size() * 1 + 6
    ) + y.size() * 2
);
"""
    assert generate_struct_get_byte_size(Dynfields[2]) == """\
return prophy::detail::nearest<4>(
    prophy::detail::nearest<4>(
        b.size() * 2 + 8
    ) + c.size() * 2 + a.size() * 2 + 4
);
"""
    assert generate_struct_get_byte_size(Dynfields[3]) == """\
return prophy::detail::nearest<8>(
    x.size() * 1 + 1
) + 16;
"""
    assert generate_struct_get_byte_size(Dynfields[4]) == """\
return y.get_byte_size() + 8;
"""
    assert generate_struct_get_byte_size(Dynfields[5]) == """\
return prophy::detail::nearest<4>(
    x.size() * 1 + 4
);
"""
    assert generate_struct_get_byte_size(Dynfields[6]) == """\
return x.get_byte_size() + y.get_byte_size() + z.get_byte_size();
"""

def test_generate_builtin_fields(Builtin):
    assert generate_struct_fields(Builtin[0]) == """\
uint32_t x;
uint32_t y;
"""
    assert generate_struct_fields(Builtin[1]) == """\
array<uint32_t, 2> x;
"""
    assert generate_struct_fields(Builtin[2]) == """\
std::vector<uint32_t> x;
"""
    assert generate_struct_fields(Builtin[3]) == """\
std::vector<uint32_t> x; /// limit 2
"""
    assert generate_struct_fields(Builtin[4]) == """\
std::vector<uint32_t> x; /// greedy
"""

def test_generate_fixcomp_fields(Fixcomp):
    assert generate_struct_fields(Fixcomp[1]) == """\
Builtin x;
Builtin y;
"""
    assert generate_struct_fields(Fixcomp[2]) == """\
array<Builtin, 2> x;
"""
    assert generate_struct_fields(Fixcomp[3]) == """\
std::vector<Builtin> x;
"""
    assert generate_struct_fields(Fixcomp[4]) == """\
std::vector<Builtin> x; /// limit 2
"""
    assert generate_struct_fields(Fixcomp[5]) == """\
std::vector<Builtin> x; /// greedy
"""

def test_generate_dyncomp_fields(Dyncomp):
    assert generate_struct_fields(Dyncomp[1]) == """\
BuiltinDynamic x;
"""
    assert generate_struct_fields(Dyncomp[2]) == """\
std::vector<BuiltinDynamic> x;
"""
    assert generate_struct_fields(Dyncomp[3]) == """\
std::vector<BuiltinDynamic> x; /// greedy
"""

def test_generate_unions_fields(Unions):
    assert generate_union_fields(Unions[1]) == """\
enum _discriminator
{
    discriminator_a = 1,
    discriminator_b = 2,
    discriminator_c = 3
} discriminator;

static const prophy::detail::int2type<discriminator_a> discriminator_a_t;
static const prophy::detail::int2type<discriminator_b> discriminator_b_t;
static const prophy::detail::int2type<discriminator_c> discriminator_c_t;

uint8_t a;
uint32_t b;
Builtin c;
"""
    assert generate_struct_fields(Unions[2]) == """\
optional<uint32_t> x;
"""
    assert generate_struct_fields(Unions[3]) == """\
optional<Builtin> x;
"""

def test_generate_enums_fields(Enums):
    assert generate_struct_fields(Enums[1]) == """\
std::vector<Enum> x;
"""
    assert generate_struct_fields(Enums[4]) == """\
array<uint16_t, CONSTANT> a;
TU16 b;
Enum c;
"""

def test_generate_floats_fields(Floats):
    assert generate_struct_fields(Floats[0]) == """\
float a;
double b;
"""

def test_generate_bytes_fields(Bytes):
    assert generate_struct_fields(Bytes[0]) == """\
array<uint8_t, 3> x;
"""
    assert generate_struct_fields(Bytes[1]) == """\
std::vector<uint8_t> x;
"""
    assert generate_struct_fields(Bytes[2]) == """\
std::vector<uint8_t> x; /// limit 4
"""
    assert generate_struct_fields(Bytes[3]) == """\
std::vector<uint8_t> x; /// greedy
"""

def test_generate_endpad_fields(Endpad):
    assert generate_struct_fields(Endpad[0]) == """\
uint16_t x;
uint8_t y;
"""
    assert generate_struct_fields(Endpad[1]) == """\
uint32_t x;
array<uint8_t, 3> y;
"""
    assert generate_struct_fields(Endpad[2]) == """\
std::vector<uint8_t> x;
"""
    assert generate_struct_fields(Endpad[3]) == """\
std::vector<uint8_t> x; /// limit 2
"""
    assert generate_struct_fields(Endpad[4]) == """\
uint32_t x;
std::vector<uint8_t> y; /// greedy
"""

def test_generate_scalarpad_fields(Scalarpad):
    assert generate_struct_fields(Scalarpad[0]) == """\
uint8_t x;
uint16_t y;
"""
    assert generate_struct_fields(Scalarpad[2]) == """\
ScalarpadComppre_Helper x;
uint16_t y;
"""
    assert generate_struct_fields(Scalarpad[4]) == """\
uint8_t x;
ScalarpadComppost_Helper y;
"""

def test_generate_unionpad_fields(Unionpad):
    assert generate_struct_fields(Unionpad[0]) == """\
uint8_t x;
optional<uint8_t> y;
"""
    assert generate_struct_fields(Unionpad[1]) == """\
optional<uint64_t> x;
"""
    assert generate_union_fields(Unionpad[2]) == """\
enum _discriminator
{
    discriminator_a = 1
} discriminator;

static const prophy::detail::int2type<discriminator_a> discriminator_a_t;

uint8_t a;
"""
    assert generate_struct_fields(Unionpad[3]) == """\
uint8_t x;
UnionpadDiscpad_Helper y;
"""
    assert generate_union_fields(Unionpad[4]) == """\
enum _discriminator
{
    discriminator_a = 1,
    discriminator_b = 2
} discriminator;

static const prophy::detail::int2type<discriminator_a> discriminator_a_t;
static const prophy::detail::int2type<discriminator_b> discriminator_b_t;

uint8_t a;
uint64_t b;
"""
    assert generate_struct_fields(Unionpad[5]) == """\
uint8_t x;
UnionpadArmpad_Helper y;
"""

def test_generate_arraypad_fields(Arraypad):
    assert generate_struct_fields(Arraypad[0]) == """\
std::vector<uint16_t> x;
"""
    assert generate_struct_fields(Arraypad[1]) == """\
uint32_t y;
std::vector<uint32_t> x;
"""
    assert generate_struct_fields(Arraypad[2]) == """\
std::vector<uint8_t> x;
"""
    assert generate_struct_fields(Arraypad[3]) == """\
uint8_t x;
ArraypadCounterAligns_Helper y;
"""
    assert generate_struct_fields(Arraypad[4]) == """\
uint32_t x;
array<uint8_t, 3> y;
uint32_t z;
"""
    assert generate_struct_fields(Arraypad[5]) == """\
std::vector<uint8_t> x;
uint32_t y;
"""
    assert generate_struct_fields(Arraypad[6]) == """\
std::vector<uint8_t> x; /// limit 2
uint32_t y;
"""

def test_generate_dynfields_fields(Dynfields):
    assert generate_struct_fields(Dynfields[0]) == """\
std::vector<uint8_t> x;
std::vector<uint16_t> y;
uint64_t z;
"""
    assert generate_struct_fields(Dynfields[1]) == """\
std::vector<uint8_t> x;
std::vector<uint16_t> y;
"""
    assert generate_struct_fields(Dynfields[2]) == """\
std::vector<uint16_t> b;
std::vector<uint16_t> c;
std::vector<uint16_t> a;
"""
    assert generate_struct_fields(Dynfields[3]) == """\
std::vector<uint8_t> x;
uint8_t y;
uint64_t z;
"""
    assert generate_struct_fields(Dynfields[4]) == """\
uint8_t x;
DynfieldsPartialpad_Helper y;
"""
    assert generate_struct_fields(Dynfields[5]) == """\
std::vector<uint8_t> x;
"""
    assert generate_struct_fields(Dynfields[6]) == """\
DynfieldsScalarpartialpad_Helper x;
DynfieldsScalarpartialpad_Helper y;
DynfieldsScalarpartialpad_Helper z;
"""

def test_generate_builtin_constructor(Builtin):
    assert generate_struct_constructor(Builtin[0]) == """\
Builtin(): x(), y() { }
Builtin(uint32_t _1, uint32_t _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Builtin[1]) == """\
BuiltinFixed(): x() { }
BuiltinFixed(const array<uint32_t, 2>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Builtin[2]) == """\
BuiltinDynamic() { }
BuiltinDynamic(const std::vector<uint32_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Builtin[3]) == """\
BuiltinLimited() { }
BuiltinLimited(const std::vector<uint32_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Builtin[4]) == """\
BuiltinGreedy() { }
BuiltinGreedy(const std::vector<uint32_t>& _1): x(_1) { }
"""

def test_generate_fixcomp_constructor(Fixcomp):
    assert generate_struct_constructor(Fixcomp[1]) == """\
Fixcomp() { }
Fixcomp(const Builtin& _1, const Builtin& _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Fixcomp[2]) == """\
FixcompFixed(): x() { }
FixcompFixed(const array<Builtin, 2>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Fixcomp[3]) == """\
FixcompDynamic() { }
FixcompDynamic(const std::vector<Builtin>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Fixcomp[4]) == """\
FixcompLimited() { }
FixcompLimited(const std::vector<Builtin>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Fixcomp[5]) == """\
FixcompGreedy() { }
FixcompGreedy(const std::vector<Builtin>& _1): x(_1) { }
"""

def test_generate_dyncomp_constructor(Dyncomp):
    assert generate_struct_constructor(Dyncomp[1]) == """\
Dyncomp() { }
Dyncomp(const BuiltinDynamic& _1): x(_1) { }
"""
    assert generate_struct_constructor(Dyncomp[2]) == """\
DyncompDynamic() { }
DyncompDynamic(const std::vector<BuiltinDynamic>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Dyncomp[3]) == """\
DyncompGreedy() { }
DyncompGreedy(const std::vector<BuiltinDynamic>& _1): x(_1) { }
"""

def test_generate_unions_constructor(Unions):
    assert generate_union_constructor(Unions[1]) == """\
Union(): discriminator(discriminator_a), a(), b() { }
Union(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }
Union(prophy::detail::int2type<discriminator_b>, uint32_t _1): discriminator(discriminator_b), b(_1) { }
Union(prophy::detail::int2type<discriminator_c>, const Builtin& _1): discriminator(discriminator_c), c(_1) { }
"""
    assert generate_struct_constructor(Unions[2]) == """\
BuiltinOptional() { }
BuiltinOptional(const optional<uint32_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Unions[3]) == """\
FixcompOptional() { }
FixcompOptional(const optional<Builtin>& _1): x(_1) { }
"""

def test_generate_enums_constructor(Enums):
    assert generate_struct_constructor(Enums[1]) == """\
DynEnum() { }
DynEnum(const std::vector<Enum>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Enums[4]) == """\
ConstantTypedefEnum(): a(), b(), c(Enum_One) { }
ConstantTypedefEnum(const array<uint16_t, CONSTANT>& _1, TU16 _2, Enum _3): a(_1), b(_2), c(_3) { }
"""

def test_generate_floats_constructor(Floats):
    assert generate_struct_constructor(Floats[0]) == """\
Floats(): a(), b() { }
Floats(float _1, double _2): a(_1), b(_2) { }
"""

def test_generate_bytes_constructor(Bytes):
    assert generate_struct_constructor(Bytes[0]) == """\
BytesFixed(): x() { }
BytesFixed(const array<uint8_t, 3>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Bytes[1]) == """\
BytesDynamic() { }
BytesDynamic(const std::vector<uint8_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Bytes[2]) == """\
BytesLimited() { }
BytesLimited(const std::vector<uint8_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Bytes[3]) == """\
BytesGreedy() { }
BytesGreedy(const std::vector<uint8_t>& _1): x(_1) { }
"""

def test_generate_endpad_constructor(Endpad):
    assert generate_struct_constructor(Endpad[0]) == """\
Endpad(): x(), y() { }
Endpad(uint16_t _1, uint8_t _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Endpad[1]) == """\
EndpadFixed(): x(), y() { }
EndpadFixed(uint32_t _1, const array<uint8_t, 3>& _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Endpad[2]) == """\
EndpadDynamic() { }
EndpadDynamic(const std::vector<uint8_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Endpad[3]) == """\
EndpadLimited() { }
EndpadLimited(const std::vector<uint8_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Endpad[4]) == """\
EndpadGreedy(): x() { }
EndpadGreedy(uint32_t _1, const std::vector<uint8_t>& _2): x(_1), y(_2) { }
"""

def test_generate_scalarpad_constructor(Scalarpad):
    assert generate_struct_constructor(Scalarpad[0]) == """\
Scalarpad(): x(), y() { }
Scalarpad(uint8_t _1, uint16_t _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Scalarpad[2]) == """\
ScalarpadComppre(): y() { }
ScalarpadComppre(const ScalarpadComppre_Helper& _1, uint16_t _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Scalarpad[4]) == """\
ScalarpadComppost(): x() { }
ScalarpadComppost(uint8_t _1, const ScalarpadComppost_Helper& _2): x(_1), y(_2) { }
"""

def test_generate_unionpad_constructor(Unionpad):
    assert generate_struct_constructor(Unionpad[0]) == """\
UnionpadOptionalboolpad(): x() { }
UnionpadOptionalboolpad(uint8_t _1, const optional<uint8_t>& _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Unionpad[1]) == """\
UnionpadOptionalvaluepad() { }
UnionpadOptionalvaluepad(const optional<uint64_t>& _1): x(_1) { }
"""
    assert generate_union_constructor(Unionpad[2]) == """\
UnionpadDiscpad_Helper(): discriminator(discriminator_a), a() { }
UnionpadDiscpad_Helper(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }
"""
    assert generate_struct_constructor(Unionpad[3]) == """\
UnionpadDiscpad(): x() { }
UnionpadDiscpad(uint8_t _1, const UnionpadDiscpad_Helper& _2): x(_1), y(_2) { }
"""
    assert generate_union_constructor(Unionpad[4]) == """\
UnionpadArmpad_Helper(): discriminator(discriminator_a), a(), b() { }
UnionpadArmpad_Helper(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }
UnionpadArmpad_Helper(prophy::detail::int2type<discriminator_b>, uint64_t _1): discriminator(discriminator_b), b(_1) { }
"""
    assert generate_struct_constructor(Unionpad[5]) == """\
UnionpadArmpad(): x() { }
UnionpadArmpad(uint8_t _1, const UnionpadArmpad_Helper& _2): x(_1), y(_2) { }
"""

def test_generate_arraypad_constructor(Arraypad):
    assert generate_struct_constructor(Arraypad[0]) == """\
ArraypadCounter() { }
ArraypadCounter(const std::vector<uint16_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Arraypad[1]) == """\
ArraypadCounterSeparated(): y() { }
ArraypadCounterSeparated(uint32_t _1, const std::vector<uint32_t>& _2): y(_1), x(_2) { }
"""
    assert generate_struct_constructor(Arraypad[2]) == """\
ArraypadCounterAligns_Helper() { }
ArraypadCounterAligns_Helper(const std::vector<uint8_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Arraypad[3]) == """\
ArraypadCounterAligns(): x() { }
ArraypadCounterAligns(uint8_t _1, const ArraypadCounterAligns_Helper& _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Arraypad[4]) == """\
ArraypadFixed(): x(), y(), z() { }
ArraypadFixed(uint32_t _1, const array<uint8_t, 3>& _2, uint32_t _3): x(_1), y(_2), z(_3) { }
"""
    assert generate_struct_constructor(Arraypad[5]) == """\
ArraypadDynamic(): y() { }
ArraypadDynamic(const std::vector<uint8_t>& _1, uint32_t _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Arraypad[6]) == """\
ArraypadLimited(): y() { }
ArraypadLimited(const std::vector<uint8_t>& _1, uint32_t _2): x(_1), y(_2) { }
"""

def test_generate_dynfields_constructor(Dynfields):
    assert generate_struct_constructor(Dynfields[0]) == """\
Dynfields(): z() { }
Dynfields(const std::vector<uint8_t>& _1, const std::vector<uint16_t>& _2, uint64_t _3): x(_1), y(_2), z(_3) { }
"""
    assert generate_struct_constructor(Dynfields[1]) == """\
DynfieldsMixed() { }
DynfieldsMixed(const std::vector<uint8_t>& _1, const std::vector<uint16_t>& _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Dynfields[2]) == """\
DynfieldsOverlapped() { }
DynfieldsOverlapped(const std::vector<uint16_t>& _1, const std::vector<uint16_t>& _2, const std::vector<uint16_t>& _3): b(_1), c(_2), a(_3) { }
"""
    assert generate_struct_constructor(Dynfields[3]) == """\
DynfieldsPartialpad_Helper(): y(), z() { }
DynfieldsPartialpad_Helper(const std::vector<uint8_t>& _1, uint8_t _2, uint64_t _3): x(_1), y(_2), z(_3) { }
"""
    assert generate_struct_constructor(Dynfields[4]) == """\
DynfieldsPartialpad(): x() { }
DynfieldsPartialpad(uint8_t _1, const DynfieldsPartialpad_Helper& _2): x(_1), y(_2) { }
"""
    assert generate_struct_constructor(Dynfields[5]) == """\
DynfieldsScalarpartialpad_Helper() { }
DynfieldsScalarpartialpad_Helper(const std::vector<uint8_t>& _1): x(_1) { }
"""
    assert generate_struct_constructor(Dynfields[6]) == """\
DynfieldsScalarpartialpad() { }
DynfieldsScalarpartialpad(const DynfieldsScalarpartialpad_Helper& _1, const DynfieldsScalarpartialpad_Helper& _2, const DynfieldsScalarpartialpad_Helper& _3): x(_1), y(_2), z(_3) { }
"""

def test_initializer_list_typedefed_enum():
    nodes = process([
        model.Enum('Enum', [
            model.EnumMember('Enum_One', '1')
        ]),
        model.Typedef('TEnum', 'Enum'),
        model.Struct('Struct', [
            model.StructMember('x', 'TEnum')
        ]),
        model.Union('Union', [
            model.UnionMember('x', 'TEnum', '1')
        ])
    ])
    assert generate_struct_constructor(nodes[2]) == """\
Struct(): x(Enum_One) { }
Struct(TEnum _1): x(_1) { }
"""
    assert generate_union_constructor(nodes[3]) == """\
Union(): discriminator(discriminator_x), x(Enum_One) { }
Union(prophy::detail::int2type<discriminator_x>, TEnum _1): discriminator(discriminator_x), x(_1) { }
"""

def test_generate_hpp_newlines():
    nodes = process([
        model.Typedef("a", "b"),
        model.Typedef("c", "d"),
        model.Enum("E1", [
            model.EnumMember("E1_A", "0")
        ]),
        model.Enum("E2", [
            model.EnumMember("E2_A", "0")
        ]),
        model.Constant("CONST_A", "0"),
        model.Typedef("e", "f"),
        model.Constant("CONST_B", "0"),
        model.Constant("CONST_C", "0"),
        model.Struct("A", [
            model.StructMember("a", "u32")
        ]),
        model.Struct("B", [
            model.StructMember("b", "u32")
        ])
    ])

    assert generate_hpp_content(nodes) == """\
typedef b a;
typedef d c;

enum E1
{
    E1_A = 0
};

enum E2
{
    E2_A = 0
};

enum { CONST_A = 0 };

typedef f e;

enum { CONST_B = 0 };
enum { CONST_C = 0 };

struct A : public prophy::detail::message<A>
{
    enum { encoded_byte_size = 4 };

    uint32_t a;

    A(): a() { }
    A(uint32_t _1): a(_1) { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct B : public prophy::detail::message<B>
{
    enum { encoded_byte_size = 4 };

    uint32_t b;

    B(): b() { }
    B(uint32_t _1): b(_1) { }

    size_t get_byte_size() const
    {
        return 4;
    }
};
"""

def test_generate_hpp(Union):
    assert generate_hpp(Union, 'MyFile') == """\
#ifndef _PROPHY_GENERATED_FULL_MyFile_HPP
#define _PROPHY_GENERATED_FULL_MyFile_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/array.hpp>
#include <prophy/endianness.hpp>
#include <prophy/optional.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>
#include <prophy/detail/mpl.hpp>

namespace prophy
{
namespace generated
{

struct X : public prophy::detail::message<X>
{
    enum { encoded_byte_size = 8 };

    enum _discriminator
    {
        discriminator_a = 1
    } discriminator;

    static const prophy::detail::int2type<discriminator_a> discriminator_a_t;

    uint8_t a;

    X(): discriminator(discriminator_a), a() { }
    X(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_MyFile_HPP */
"""

def test_generate_cpp(Struct):
    assert generate_cpp(Struct, 'MyFile') == """\
#include "MyFile.ppf.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include <prophy/detail/printer.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy::generated;

namespace prophy
{
namespace detail
{

template <>
template <endianness E>
uint8_t* message_impl<X>::encode(const X& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<X>::encode<native>(const X& x, uint8_t* pos);
template uint8_t* message_impl<X>::encode<little>(const X& x, uint8_t* pos);
template uint8_t* message_impl<X>::encode<big>(const X& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<X>::decode(X& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<X>::decode<native>(X& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<X>::decode<little>(X& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<X>::decode<big>(X& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<X>::print(const X& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "x", x.x);
    do_print(out, indent, "y", x.y);
}
template void message_impl<X>::print(const X& x, std::ostream& out, size_t indent);

template <>
template <endianness E>
uint8_t* message_impl<Y>::encode(const Y& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
    return pos;
}
template uint8_t* message_impl<Y>::encode<native>(const Y& x, uint8_t* pos);
template uint8_t* message_impl<Y>::encode<little>(const Y& x, uint8_t* pos);
template uint8_t* message_impl<Y>::encode<big>(const Y& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Y>::decode(Y& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end)
    );
}
template bool message_impl<Y>::decode<native>(Y& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Y>::decode<little>(Y& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Y>::decode<big>(Y& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Y>::print(const Y& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "x", x.x.data(), x.x.size());
}
template void message_impl<Y>::print(const Y& x, std::ostream& out, size_t indent);

} // namespace detail
} // namespace prophy
"""

def test_generate_hpp_with_included_struct():
    nodes = process([
        model.Include('Input', process([
            model.Struct('X', [
                model.StructMember('x', 'u64'),
            ])
        ])),
        model.Struct('Y', [
            model.StructMember('x', 'X')
        ])
    ])

    assert """\
#include "Input.ppf.hpp"

namespace prophy
{
namespace generated
{

struct Y : public prophy::detail::message<Y>
{
    enum { encoded_byte_size = 8 };

    X x;

    Y() { }
    Y(const X& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

} // namespace generated
} // namespace prophy
""" in generate_hpp(nodes, 'MyFile')

def test_exception_when_byte_size_is_unknown(tmpdir_cwd):
    nodes = process([
        model.Struct('X', [
            model.StructMember('x', 'Unknown')
        ])
    ])
    with pytest.raises(GenerateError) as e:
        CppFullGenerator('.').serialize(nodes, 'Filename')
    assert "X byte size unknown" == str(e.value)

def test_exception_when_numeric_size_is_unknown(tmpdir_cwd):
    nodes = process([
        model.Struct('X', [
            model.StructMember('x', 'u32', size = 'Unknown')
        ])
    ])
    with pytest.raises(GenerateError) as e:
        CppFullGenerator('.').serialize(nodes, 'Filename')
    assert "X byte size unknown" == str(e.value)

def test_exception_when_union_byte_size_is_unknown(tmpdir_cwd):
    nodes = process([
        model.Union('X', [
            model.UnionMember('x', 'StillUnknown', '1')
        ])
    ])
    with pytest.raises(GenerateError) as e:
        CppFullGenerator('.').serialize(nodes, 'Filename')
    assert "X byte size unknown" == str(e.value)

def test_exception_when_multiple_arrays_are_bounded_by_the_same_member(tmpdir_cwd):
    nodes = process([
        model.Struct('X', [
            model.StructMember('num_of_elements', 'u32'),
            model.StructMember('array1', 'u32', bound = 'num_of_elements'),
            model.StructMember('array2', 'u32', bound = 'num_of_elements'),
        ])
    ])
    with pytest.raises(GenerateError) as e:
        CppFullGenerator('.').serialize(nodes, 'Filename')
    assert "Multiple arrays bounded by the same member (num_of_elements) in struct X is unsupported" == str(e.value)

def test_get_byte_size_when_array_delimiter_is_a_typedef():
    nodes = process([
        model.Typedef('IntType', 'u32'),
        model.Struct('X', [
            model.StructMember('num_of_x', 'u32'),
            model.StructMember('x', 'IntType', bound = 'num_of_x')
        ])
    ])
    assert 'x.size() * 4 + 4' in generate_struct_get_byte_size(nodes[1])

def test_encode_and_decode_when_array_delimiter_is_a_typedef():
    nodes = process([
        model.Typedef('IntType', 'u32'),
        model.Struct('X', [
            model.StructMember('num_of_x', 'IntType'),
            model.StructMember('x', 'u32', bound = 'num_of_x')
        ])
    ])
    assert 'uint32_t(x.x.size())' in generate_struct_encode(nodes[1])
    assert 'do_decode_resize<E, uint32_t>' in generate_struct_decode(nodes[1])
