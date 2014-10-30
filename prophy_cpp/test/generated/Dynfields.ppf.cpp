#include "Dynfields.ppf.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy::generated;

namespace prophy
{
namespace detail
{

template <>
template <endianness E>
uint8_t* message_impl<Dynfields>::encode(const Dynfields& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
    pos = align<2>(pos);
    pos = do_encode<E>(pos, uint16_t(x.y.size()));
    pos = do_encode<E>(pos, x.y.data(), uint16_t(x.y.size()));
    pos = align<8>(pos);
    pos = do_encode<E>(pos, x.z);
    return pos;
}
template uint8_t* message_impl<Dynfields>::encode<native>(const Dynfields& x, uint8_t* pos);
template uint8_t* message_impl<Dynfields>::encode<little>(const Dynfields& x, uint8_t* pos);
template uint8_t* message_impl<Dynfields>::encode<big>(const Dynfields& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Dynfields>::decode(Dynfields& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_align<2>(pos, end) &&
        do_decode_resize<E, uint16_t>(x.y, pos, end) &&
        do_decode<E>(x.y.data(), x.y.size(), pos, end) &&
        do_decode_align<8>(pos, end) &&
        do_decode<E>(x.z, pos, end)
    );
}
template bool message_impl<Dynfields>::decode<native>(Dynfields& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Dynfields>::decode<little>(Dynfields& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Dynfields>::decode<big>(Dynfields& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<DynfieldsMixed>::encode(const DynfieldsMixed& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, uint16_t(x.y.size()));
    pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
    pos = align<2>(pos);
    pos = do_encode<E>(pos, x.y.data(), uint16_t(x.y.size()));
    pos = align<4>(pos);
    return pos;
}
template uint8_t* message_impl<DynfieldsMixed>::encode<native>(const DynfieldsMixed& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsMixed>::encode<little>(const DynfieldsMixed& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsMixed>::encode<big>(const DynfieldsMixed& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<DynfieldsMixed>::decode(DynfieldsMixed& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode_resize<E, uint16_t>(x.y, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_align<2>(pos, end) &&
        do_decode<E>(x.y.data(), x.y.size(), pos, end) &&
        do_decode_align<4>(pos, end)
    );
}
template bool message_impl<DynfieldsMixed>::decode<native>(DynfieldsMixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsMixed>::decode<little>(DynfieldsMixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsMixed>::decode<big>(DynfieldsMixed& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<DynfieldsOverlapped>::encode(const DynfieldsOverlapped& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.a.size()));
    pos = do_encode<E>(pos, uint32_t(x.b.size()));
    pos = do_encode<E>(pos, x.b.data(), uint32_t(x.b.size()));
    pos = align<4>(pos);
    pos = do_encode<E>(pos, uint32_t(x.c.size()));
    pos = do_encode<E>(pos, x.c.data(), uint32_t(x.c.size()));
    pos = do_encode<E>(pos, x.a.data(), uint32_t(x.a.size()));
    pos = align<4>(pos);
    return pos;
}
template uint8_t* message_impl<DynfieldsOverlapped>::encode<native>(const DynfieldsOverlapped& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsOverlapped>::encode<little>(const DynfieldsOverlapped& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsOverlapped>::encode<big>(const DynfieldsOverlapped& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<DynfieldsOverlapped>::decode(DynfieldsOverlapped& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.a, pos, end) &&
        do_decode_resize<E, uint32_t>(x.b, pos, end) &&
        do_decode<E>(x.b.data(), x.b.size(), pos, end) &&
        do_decode_align<4>(pos, end) &&
        do_decode_resize<E, uint32_t>(x.c, pos, end) &&
        do_decode<E>(x.c.data(), x.c.size(), pos, end) &&
        do_decode<E>(x.a.data(), x.a.size(), pos, end) &&
        do_decode_align<4>(pos, end)
    );
}
template bool message_impl<DynfieldsOverlapped>::decode<native>(DynfieldsOverlapped& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsOverlapped>::decode<little>(DynfieldsOverlapped& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsOverlapped>::decode<big>(DynfieldsOverlapped& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<DynfieldsPartialpad_Helper>::encode(const DynfieldsPartialpad_Helper& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint8_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
    pos = align<8>(pos);
    pos = do_encode<E>(pos, x.y);
    pos = pos + 7;
    pos = do_encode<E>(pos, x.z);
    return pos;
}
template uint8_t* message_impl<DynfieldsPartialpad_Helper>::encode<native>(const DynfieldsPartialpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsPartialpad_Helper>::encode<little>(const DynfieldsPartialpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsPartialpad_Helper>::encode<big>(const DynfieldsPartialpad_Helper& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<DynfieldsPartialpad_Helper>::decode(DynfieldsPartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint8_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_align<8>(pos, end) &&
        do_decode<E>(x.y, pos, end) &&
        do_decode_advance(7, pos, end) &&
        do_decode<E>(x.z, pos, end)
    );
}
template bool message_impl<DynfieldsPartialpad_Helper>::decode<native>(DynfieldsPartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsPartialpad_Helper>::decode<little>(DynfieldsPartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsPartialpad_Helper>::decode<big>(DynfieldsPartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<DynfieldsPartialpad>::encode(const DynfieldsPartialpad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 7;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<DynfieldsPartialpad>::encode<native>(const DynfieldsPartialpad& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsPartialpad>::encode<little>(const DynfieldsPartialpad& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsPartialpad>::encode<big>(const DynfieldsPartialpad& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<DynfieldsPartialpad>::decode(DynfieldsPartialpad& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode_advance(7, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<DynfieldsPartialpad>::decode<native>(DynfieldsPartialpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsPartialpad>::decode<little>(DynfieldsPartialpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsPartialpad>::decode<big>(DynfieldsPartialpad& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<DynfieldsScalarpartialpad_Helper>::encode(const DynfieldsScalarpartialpad_Helper& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
    pos = align<4>(pos);
    return pos;
}
template uint8_t* message_impl<DynfieldsScalarpartialpad_Helper>::encode<native>(const DynfieldsScalarpartialpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsScalarpartialpad_Helper>::encode<little>(const DynfieldsScalarpartialpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsScalarpartialpad_Helper>::encode<big>(const DynfieldsScalarpartialpad_Helper& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<DynfieldsScalarpartialpad_Helper>::decode(DynfieldsScalarpartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_align<4>(pos, end)
    );
}
template bool message_impl<DynfieldsScalarpartialpad_Helper>::decode<native>(DynfieldsScalarpartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsScalarpartialpad_Helper>::decode<little>(DynfieldsScalarpartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsScalarpartialpad_Helper>::decode<big>(DynfieldsScalarpartialpad_Helper& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<DynfieldsScalarpartialpad>::encode(const DynfieldsScalarpartialpad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y);
    pos = do_encode<E>(pos, x.z);
    return pos;
}
template uint8_t* message_impl<DynfieldsScalarpartialpad>::encode<native>(const DynfieldsScalarpartialpad& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsScalarpartialpad>::encode<little>(const DynfieldsScalarpartialpad& x, uint8_t* pos);
template uint8_t* message_impl<DynfieldsScalarpartialpad>::encode<big>(const DynfieldsScalarpartialpad& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<DynfieldsScalarpartialpad>::decode(DynfieldsScalarpartialpad& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode<E>(x.y, pos, end) &&
        do_decode<E>(x.z, pos, end)
    );
}
template bool message_impl<DynfieldsScalarpartialpad>::decode<native>(DynfieldsScalarpartialpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsScalarpartialpad>::decode<little>(DynfieldsScalarpartialpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<DynfieldsScalarpartialpad>::decode<big>(DynfieldsScalarpartialpad& x, const uint8_t*& pos, const uint8_t* end);

} // namespace detail
} // namespace prophy
