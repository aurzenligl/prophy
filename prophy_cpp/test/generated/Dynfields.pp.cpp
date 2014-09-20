#include "Dynfields.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

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

} // namespace detail
} // namespace prophy
