#include "Unions.ppf.hpp"
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
uint8_t* message_impl<Union>::encode(const Union& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.discriminator);
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
bool message_impl<Union>::decode(Union& x, const uint8_t*& pos, const uint8_t* end)
{
    if (!do_decode<E>(x.discriminator, pos, end)) return false;
    switch(x.discriminator)
    {
        case Union::discriminator_a: if (!do_decode_in_place<E>(x.a, pos, end)) return false; break;
        case Union::discriminator_b: if (!do_decode_in_place<E>(x.b, pos, end)) return false; break;
        case Union::discriminator_c: if (!do_decode_in_place<E>(x.c, pos, end)) return false; break;
        default: return false;
    }
    return do_decode_advance(8, pos, end);
}
template bool message_impl<Union>::decode<native>(Union& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Union>::decode<little>(Union& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Union>::decode<big>(Union& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Union>::print(const Union& x, std::ostream& out, size_t indent)
{
    switch(x.discriminator)
    {
        case Union::discriminator_a: do_print(out, indent, "a", x.a); break;
        case Union::discriminator_b: do_print(out, indent, "b", x.b); break;
        case Union::discriminator_c: do_print(out, indent, "c", x.c); break;
    }
}
template void message_impl<Union>::print(const Union& x, std::ostream& out, size_t indent);

template <>
template <endianness E>
uint8_t* message_impl<BuiltinOptional>::encode(const BuiltinOptional& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.has_x);
    if (x.has_x) do_encode<E>(pos, x.x);
    pos = pos + 4;
    return pos;
}
template uint8_t* message_impl<BuiltinOptional>::encode<native>(const BuiltinOptional& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinOptional>::encode<little>(const BuiltinOptional& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinOptional>::encode<big>(const BuiltinOptional& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<BuiltinOptional>::decode(BuiltinOptional& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.has_x, pos, end) &&
        do_decode_in_place_optional<E>(x.x, x.has_x, pos, end) &&
        do_decode_advance(4, pos, end)
    );
}
template bool message_impl<BuiltinOptional>::decode<native>(BuiltinOptional& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinOptional>::decode<little>(BuiltinOptional& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinOptional>::decode<big>(BuiltinOptional& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<BuiltinOptional>::print(const BuiltinOptional& x, std::ostream& out, size_t indent)
{
    if (x.has_x) do_print(out, indent, "x", x.x);
}
template void message_impl<BuiltinOptional>::print(const BuiltinOptional& x, std::ostream& out, size_t indent);

template <>
template <endianness E>
uint8_t* message_impl<FixcompOptional>::encode(const FixcompOptional& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.has_x);
    if (x.has_x) do_encode<E>(pos, x.x);
    pos = pos + 8;
    return pos;
}
template uint8_t* message_impl<FixcompOptional>::encode<native>(const FixcompOptional& x, uint8_t* pos);
template uint8_t* message_impl<FixcompOptional>::encode<little>(const FixcompOptional& x, uint8_t* pos);
template uint8_t* message_impl<FixcompOptional>::encode<big>(const FixcompOptional& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<FixcompOptional>::decode(FixcompOptional& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.has_x, pos, end) &&
        do_decode_in_place_optional<E>(x.x, x.has_x, pos, end) &&
        do_decode_advance(8, pos, end)
    );
}
template bool message_impl<FixcompOptional>::decode<native>(FixcompOptional& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompOptional>::decode<little>(FixcompOptional& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompOptional>::decode<big>(FixcompOptional& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<FixcompOptional>::print(const FixcompOptional& x, std::ostream& out, size_t indent)
{
    if (x.has_x) do_print(out, indent, "x", x.x);
}
template void message_impl<FixcompOptional>::print(const FixcompOptional& x, std::ostream& out, size_t indent);

} // namespace detail
} // namespace prophy
