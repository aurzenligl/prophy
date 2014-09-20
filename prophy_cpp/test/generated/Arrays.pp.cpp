#include "Arrays.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include <prophy/detail/align.hpp>

namespace prophy
{
namespace detail
{

template <>
template <endianness E>
uint8_t* message_impl<Builtin>::encode(const Builtin& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<Builtin>::encode<native>(const Builtin& x, uint8_t* pos);
template uint8_t* message_impl<Builtin>::encode<little>(const Builtin& x, uint8_t* pos);
template uint8_t* message_impl<Builtin>::encode<big>(const Builtin& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Builtin>::decode(Builtin& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<Builtin>::decode<native>(Builtin& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Builtin>::decode<little>(Builtin& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Builtin>::decode<big>(Builtin& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<BuiltinFixed>::encode(const BuiltinFixed& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x, 2);
    return pos;
}
template uint8_t* message_impl<BuiltinFixed>::encode<native>(const BuiltinFixed& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinFixed>::encode<little>(const BuiltinFixed& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinFixed>::encode<big>(const BuiltinFixed& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<BuiltinFixed>::decode(BuiltinFixed& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, 2, pos, end)
    );
}
template bool message_impl<BuiltinFixed>::decode<native>(BuiltinFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinFixed>::decode<little>(BuiltinFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinFixed>::decode<big>(BuiltinFixed& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<BuiltinDynamic>::encode(const BuiltinDynamic& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    return pos;
}
template uint8_t* message_impl<BuiltinDynamic>::encode<native>(const BuiltinDynamic& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinDynamic>::encode<little>(const BuiltinDynamic& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinDynamic>::encode<big>(const BuiltinDynamic& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<BuiltinDynamic>::decode(BuiltinDynamic& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end)
    );
}
template bool message_impl<BuiltinDynamic>::decode<native>(BuiltinDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinDynamic>::decode<little>(BuiltinDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinDynamic>::decode<big>(BuiltinDynamic& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<BuiltinLimited>::encode(const BuiltinLimited& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
    do_encode<E>(pos, x.x.data(), std::min(x.x.size(), size_t(2)));
    pos = pos + 8;
    return pos;
}
template uint8_t* message_impl<BuiltinLimited>::encode<native>(const BuiltinLimited& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinLimited>::encode<little>(const BuiltinLimited& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinLimited>::encode<big>(const BuiltinLimited& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<BuiltinLimited>::decode(BuiltinLimited& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end, 2) &&
        do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_advance(8, pos, end)
    );
}
template bool message_impl<BuiltinLimited>::decode<native>(BuiltinLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinLimited>::decode<little>(BuiltinLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinLimited>::decode<big>(BuiltinLimited& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<BuiltinGreedy>::encode(const BuiltinGreedy& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    return pos;
}
template uint8_t* message_impl<BuiltinGreedy>::encode<native>(const BuiltinGreedy& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinGreedy>::encode<little>(const BuiltinGreedy& x, uint8_t* pos);
template uint8_t* message_impl<BuiltinGreedy>::encode<big>(const BuiltinGreedy& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<BuiltinGreedy>::decode(BuiltinGreedy& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_greedy<E>(x.x, pos, end)
    );
}
template bool message_impl<BuiltinGreedy>::decode<native>(BuiltinGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinGreedy>::decode<little>(BuiltinGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BuiltinGreedy>::decode<big>(BuiltinGreedy& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<Fixcomp>::encode(const Fixcomp& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<Fixcomp>::encode<native>(const Fixcomp& x, uint8_t* pos);
template uint8_t* message_impl<Fixcomp>::encode<little>(const Fixcomp& x, uint8_t* pos);
template uint8_t* message_impl<Fixcomp>::encode<big>(const Fixcomp& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Fixcomp>::decode(Fixcomp& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<Fixcomp>::decode<native>(Fixcomp& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Fixcomp>::decode<little>(Fixcomp& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Fixcomp>::decode<big>(Fixcomp& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<FixcompFixed>::encode(const FixcompFixed& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x, 2);
    return pos;
}
template uint8_t* message_impl<FixcompFixed>::encode<native>(const FixcompFixed& x, uint8_t* pos);
template uint8_t* message_impl<FixcompFixed>::encode<little>(const FixcompFixed& x, uint8_t* pos);
template uint8_t* message_impl<FixcompFixed>::encode<big>(const FixcompFixed& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<FixcompFixed>::decode(FixcompFixed& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, 2, pos, end)
    );
}
template bool message_impl<FixcompFixed>::decode<native>(FixcompFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompFixed>::decode<little>(FixcompFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompFixed>::decode<big>(FixcompFixed& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<FixcompDynamic>::encode(const FixcompDynamic& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    return pos;
}
template uint8_t* message_impl<FixcompDynamic>::encode<native>(const FixcompDynamic& x, uint8_t* pos);
template uint8_t* message_impl<FixcompDynamic>::encode<little>(const FixcompDynamic& x, uint8_t* pos);
template uint8_t* message_impl<FixcompDynamic>::encode<big>(const FixcompDynamic& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<FixcompDynamic>::decode(FixcompDynamic& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end)
    );
}
template bool message_impl<FixcompDynamic>::decode<native>(FixcompDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompDynamic>::decode<little>(FixcompDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompDynamic>::decode<big>(FixcompDynamic& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<FixcompLimited>::encode(const FixcompLimited& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
    do_encode<E>(pos, x.x.data(), std::min(x.x.size(), size_t(2)));
    pos = pos + 16;
    return pos;
}
template uint8_t* message_impl<FixcompLimited>::encode<native>(const FixcompLimited& x, uint8_t* pos);
template uint8_t* message_impl<FixcompLimited>::encode<little>(const FixcompLimited& x, uint8_t* pos);
template uint8_t* message_impl<FixcompLimited>::encode<big>(const FixcompLimited& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<FixcompLimited>::decode(FixcompLimited& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end, 2) &&
        do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_advance(16, pos, end)
    );
}
template bool message_impl<FixcompLimited>::decode<native>(FixcompLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompLimited>::decode<little>(FixcompLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompLimited>::decode<big>(FixcompLimited& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<FixcompGreedy>::encode(const FixcompGreedy& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    return pos;
}
template uint8_t* message_impl<FixcompGreedy>::encode<native>(const FixcompGreedy& x, uint8_t* pos);
template uint8_t* message_impl<FixcompGreedy>::encode<little>(const FixcompGreedy& x, uint8_t* pos);
template uint8_t* message_impl<FixcompGreedy>::encode<big>(const FixcompGreedy& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<FixcompGreedy>::decode(FixcompGreedy& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_greedy<E>(x.x, pos, end)
    );
}
template bool message_impl<FixcompGreedy>::decode<native>(FixcompGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompGreedy>::decode<little>(FixcompGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<FixcompGreedy>::decode<big>(FixcompGreedy& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<Dyncomp>::encode(const Dyncomp& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    return pos;
}
template uint8_t* message_impl<Dyncomp>::encode<native>(const Dyncomp& x, uint8_t* pos);
template uint8_t* message_impl<Dyncomp>::encode<little>(const Dyncomp& x, uint8_t* pos);
template uint8_t* message_impl<Dyncomp>::encode<big>(const Dyncomp& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<DyncompDynamic>::encode(const DyncompDynamic& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    return pos;
}
template uint8_t* message_impl<DyncompDynamic>::encode<native>(const DyncompDynamic& x, uint8_t* pos);
template uint8_t* message_impl<DyncompDynamic>::encode<little>(const DyncompDynamic& x, uint8_t* pos);
template uint8_t* message_impl<DyncompDynamic>::encode<big>(const DyncompDynamic& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<DyncompGreedy>::encode(const DyncompGreedy& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    return pos;
}
template uint8_t* message_impl<DyncompGreedy>::encode<native>(const DyncompGreedy& x, uint8_t* pos);
template uint8_t* message_impl<DyncompGreedy>::encode<little>(const DyncompGreedy& x, uint8_t* pos);
template uint8_t* message_impl<DyncompGreedy>::encode<big>(const DyncompGreedy& x, uint8_t* pos);

} // namespace detail
} // namespace prophy
