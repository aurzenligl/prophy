#include "Unions.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

namespace prophy
{
namespace detail
{

template <>
template <endianness E>
uint8_t* message_impl<Union>::encode(const Union& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.discriminator));
    switch(x.discriminator)
    {
        case Union::discriminator_a: do_encode<E>(pos, x.a); break;
        case Union::discriminator_b: do_encode<E>(pos, x.b); break;
        case Union::discriminator_c: do_encode<E>(pos, x.c); break;
    }
    pos = pos + 8;
    return pos;
}
template uint8_t* message_impl<Union>::encode<native>(const Union& x, uint8_t* pos);
template uint8_t* message_impl<Union>::encode<little>(const Union& x, uint8_t* pos);
template uint8_t* message_impl<Union>::encode<big>(const Union& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<BuiltinOptional>::encode(const BuiltinOptional& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.has_x));
    if (x.has_x) do_encode<E>(pos, x.x);
    pos = pos + 4;
    return pos;
}
template uint8_t* message_impl<BuiltinOptional>::encode<native>(const BuiltinOptional& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinOptional>::encode<little>(const BuiltinOptional& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinOptional>::encode<big>(const BuiltinOptional& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<FixcompOptional>::encode(const FixcompOptional& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.has_x));
    if (x.has_x) do_encode<E>(pos, x.x);
    pos = pos + 8;
    return pos;
}
template uint8_t* message_impl<FixcompOptional>::encode<native>(const FixcompOptional& x, uint8_t* pos);
template uint8_t* message_impl<FixcompOptional>::encode<little>(const FixcompOptional& x, uint8_t* pos);
template uint8_t* message_impl<FixcompOptional>::encode<big>(const FixcompOptional& x, uint8_t* pos);

} // namespace detail
} // namespace prophy
