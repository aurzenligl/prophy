#include "Paddings.pp.hpp"
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
uint8_t* message_impl<Endpad>::encode(const Endpad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y);
    pos = pos + 1;
    return pos;
}
template uint8_t* message_impl<Endpad>::encode<native>(const Endpad& x, uint8_t* pos);
template uint8_t* message_impl<Endpad>::encode<little>(const Endpad& x, uint8_t* pos);
template uint8_t* message_impl<Endpad>::encode<big>(const Endpad& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Endpad>::decode(Endpad& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode<E>(x.y, pos, end) &&
        do_decode_advance(1, pos, end)
    );
}
template bool message_impl<Endpad>::decode<native>(Endpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Endpad>::decode<little>(Endpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Endpad>::decode<big>(Endpad& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<EndpadFixed>::encode(const EndpadFixed& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y, 3);
    pos = pos + 1;
    return pos;
}
template uint8_t* message_impl<EndpadFixed>::encode<native>(const EndpadFixed& x, uint8_t* pos);
template uint8_t* message_impl<EndpadFixed>::encode<little>(const EndpadFixed& x, uint8_t* pos);
template uint8_t* message_impl<EndpadFixed>::encode<big>(const EndpadFixed& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<EndpadFixed>::decode(EndpadFixed& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode<E>(x.y, 3, pos, end) &&
        do_decode_advance(1, pos, end)
    );
}
template bool message_impl<EndpadFixed>::decode<native>(EndpadFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadFixed>::decode<little>(EndpadFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadFixed>::decode<big>(EndpadFixed& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<EndpadDynamic>::encode(const EndpadDynamic& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
    pos = align<4>(pos);
    return pos;
}
template uint8_t* message_impl<EndpadDynamic>::encode<native>(const EndpadDynamic& x, uint8_t* pos);
template uint8_t* message_impl<EndpadDynamic>::encode<little>(const EndpadDynamic& x, uint8_t* pos);
template uint8_t* message_impl<EndpadDynamic>::encode<big>(const EndpadDynamic& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<EndpadDynamic>::decode(EndpadDynamic& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_align<4>(pos, end)
    );
}
template bool message_impl<EndpadDynamic>::decode<native>(EndpadDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadDynamic>::decode<little>(EndpadDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadDynamic>::decode<big>(EndpadDynamic& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<EndpadLimited>::encode(const EndpadLimited& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
    do_encode<E>(pos, x.x.data(), std::min(x.x.size(), size_t(2)));
    pos = pos + 2;
    pos = pos + 2;
    return pos;
}
template uint8_t* message_impl<EndpadLimited>::encode<native>(const EndpadLimited& x, uint8_t* pos);
template uint8_t* message_impl<EndpadLimited>::encode<little>(const EndpadLimited& x, uint8_t* pos);
template uint8_t* message_impl<EndpadLimited>::encode<big>(const EndpadLimited& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<EndpadLimited>::decode(EndpadLimited& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end, 2) &&
        do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_advance(2, pos, end) &&
        do_decode_advance(2, pos, end)
    );
}
template bool message_impl<EndpadLimited>::decode<native>(EndpadLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadLimited>::decode<little>(EndpadLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadLimited>::decode<big>(EndpadLimited& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<EndpadGreedy>::encode(const EndpadGreedy& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x));
    pos = do_encode<E>(pos, x.y.data(), x.y.size());
    pos = align<4>(pos);
    return pos;
}
template uint8_t* message_impl<EndpadGreedy>::encode<native>(const EndpadGreedy& x, uint8_t* pos);
template uint8_t* message_impl<EndpadGreedy>::encode<little>(const EndpadGreedy& x, uint8_t* pos);
template uint8_t* message_impl<EndpadGreedy>::encode<big>(const EndpadGreedy& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<EndpadGreedy>::decode(EndpadGreedy& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode_greedy<E>(x.y, pos, end) &&
        do_decode_align<4>(pos, end)
    );
}
template bool message_impl<EndpadGreedy>::decode<native>(EndpadGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadGreedy>::decode<little>(EndpadGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<EndpadGreedy>::decode<big>(EndpadGreedy& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<Scalarpad>::encode(const Scalarpad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 1;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<Scalarpad>::encode<native>(const Scalarpad& x, uint8_t* pos);
template uint8_t* message_impl<Scalarpad>::encode<little>(const Scalarpad& x, uint8_t* pos);
template uint8_t* message_impl<Scalarpad>::encode<big>(const Scalarpad& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Scalarpad>::decode(Scalarpad& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode_advance(1, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<Scalarpad>::decode<native>(Scalarpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Scalarpad>::decode<little>(Scalarpad& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Scalarpad>::decode<big>(Scalarpad& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<ScalarpadComppre_Helper>::encode(const ScalarpadComppre_Helper& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    return pos;
}
template uint8_t* message_impl<ScalarpadComppre_Helper>::encode<native>(const ScalarpadComppre_Helper& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppre_Helper>::encode<little>(const ScalarpadComppre_Helper& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppre_Helper>::encode<big>(const ScalarpadComppre_Helper& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<ScalarpadComppre_Helper>::decode(ScalarpadComppre_Helper& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end)
    );
}
template bool message_impl<ScalarpadComppre_Helper>::decode<native>(ScalarpadComppre_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppre_Helper>::decode<little>(ScalarpadComppre_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppre_Helper>::decode<big>(ScalarpadComppre_Helper& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<ScalarpadComppre>::encode(const ScalarpadComppre& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 1;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<ScalarpadComppre>::encode<native>(const ScalarpadComppre& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppre>::encode<little>(const ScalarpadComppre& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppre>::encode<big>(const ScalarpadComppre& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<ScalarpadComppre>::decode(ScalarpadComppre& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode_advance(1, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<ScalarpadComppre>::decode<native>(ScalarpadComppre& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppre>::decode<little>(ScalarpadComppre& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppre>::decode<big>(ScalarpadComppre& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<ScalarpadComppost_Helper>::encode(const ScalarpadComppost_Helper& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    return pos;
}
template uint8_t* message_impl<ScalarpadComppost_Helper>::encode<native>(const ScalarpadComppost_Helper& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppost_Helper>::encode<little>(const ScalarpadComppost_Helper& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppost_Helper>::encode<big>(const ScalarpadComppost_Helper& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<ScalarpadComppost_Helper>::decode(ScalarpadComppost_Helper& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end)
    );
}
template bool message_impl<ScalarpadComppost_Helper>::decode<native>(ScalarpadComppost_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppost_Helper>::decode<little>(ScalarpadComppost_Helper& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppost_Helper>::decode<big>(ScalarpadComppost_Helper& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<ScalarpadComppost>::encode(const ScalarpadComppost& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 1;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<ScalarpadComppost>::encode<native>(const ScalarpadComppost& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppost>::encode<little>(const ScalarpadComppost& x, uint8_t* pos);
template uint8_t* message_impl<ScalarpadComppost>::encode<big>(const ScalarpadComppost& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<ScalarpadComppost>::decode(ScalarpadComppost& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, pos, end) &&
        do_decode_advance(1, pos, end) &&
        do_decode<E>(x.y, pos, end)
    );
}
template bool message_impl<ScalarpadComppost>::decode<native>(ScalarpadComppost& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppost>::decode<little>(ScalarpadComppost& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ScalarpadComppost>::decode<big>(ScalarpadComppost& x, const uint8_t*& pos, const uint8_t* end);

template <>
template <endianness E>
uint8_t* message_impl<UnionpadOptionalboolpad>::encode(const UnionpadOptionalboolpad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 3;
    pos = do_encode<E>(pos, uint32_t(x.has_y));
    pos = do_encode<E>(pos, x.y);
    pos = pos + 3;
    return pos;
}
template uint8_t* message_impl<UnionpadOptionalboolpad>::encode<native>(const UnionpadOptionalboolpad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadOptionalboolpad>::encode<little>(const UnionpadOptionalboolpad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadOptionalboolpad>::encode<big>(const UnionpadOptionalboolpad& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<UnionpadOptionalvaluepad>::encode(const UnionpadOptionalvaluepad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.has_x));
    pos = pos + 4;
    pos = do_encode<E>(pos, x.x);
    return pos;
}
template uint8_t* message_impl<UnionpadOptionalvaluepad>::encode<native>(const UnionpadOptionalvaluepad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadOptionalvaluepad>::encode<little>(const UnionpadOptionalvaluepad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadOptionalvaluepad>::encode<big>(const UnionpadOptionalvaluepad& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<UnionpadDiscpad_Helper>::encode(const UnionpadDiscpad_Helper& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.discriminator));
    switch(x.discriminator)
    {
        case UnionpadDiscpad_Helper::discriminator_a: do_encode<E>(pos, x.a); break;
    }
    pos = pos + 4;
    return pos;
}
template uint8_t* message_impl<UnionpadDiscpad_Helper>::encode<native>(const UnionpadDiscpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadDiscpad_Helper>::encode<little>(const UnionpadDiscpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadDiscpad_Helper>::encode<big>(const UnionpadDiscpad_Helper& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<UnionpadDiscpad>::encode(const UnionpadDiscpad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 3;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<UnionpadDiscpad>::encode<native>(const UnionpadDiscpad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadDiscpad>::encode<little>(const UnionpadDiscpad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadDiscpad>::encode<big>(const UnionpadDiscpad& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<UnionpadArmpad_Helper>::encode(const UnionpadArmpad_Helper& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.discriminator));
    pos = pos + 4;
    switch(x.discriminator)
    {
        case UnionpadArmpad_Helper::discriminator_a: do_encode<E>(pos, x.a); break;
        case UnionpadArmpad_Helper::discriminator_b: do_encode<E>(pos, x.b); break;
    }
    pos = pos + 8;
    return pos;
}
template uint8_t* message_impl<UnionpadArmpad_Helper>::encode<native>(const UnionpadArmpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadArmpad_Helper>::encode<little>(const UnionpadArmpad_Helper& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadArmpad_Helper>::encode<big>(const UnionpadArmpad_Helper& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<UnionpadArmpad>::encode(const UnionpadArmpad& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 7;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<UnionpadArmpad>::encode<native>(const UnionpadArmpad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadArmpad>::encode<little>(const UnionpadArmpad& x, uint8_t* pos);
template uint8_t* message_impl<UnionpadArmpad>::encode<big>(const UnionpadArmpad& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<ArraypadCounter>::encode(const ArraypadCounter& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint8_t(x.x.size()));
    pos = pos + 1;
    pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
    return pos;
}
template uint8_t* message_impl<ArraypadCounter>::encode<native>(const ArraypadCounter& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounter>::encode<little>(const ArraypadCounter& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounter>::encode<big>(const ArraypadCounter& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<ArraypadCounterSeparated>::encode(const ArraypadCounterSeparated& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint8_t(x.x.size()));
    pos = pos + 3;
    pos = do_encode<E>(pos, x.y);
    pos = do_encode<E>(pos, x.x.data(), uint8_t(x.x.size()));
    return pos;
}
template uint8_t* message_impl<ArraypadCounterSeparated>::encode<native>(const ArraypadCounterSeparated& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounterSeparated>::encode<little>(const ArraypadCounterSeparated& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounterSeparated>::encode<big>(const ArraypadCounterSeparated& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<ArraypadCounterAligns_Helper>::encode(const ArraypadCounterAligns_Helper& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint16_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint16_t(x.x.size()));
    pos = align<2>(pos);
    return pos;
}
template uint8_t* message_impl<ArraypadCounterAligns_Helper>::encode<native>(const ArraypadCounterAligns_Helper& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounterAligns_Helper>::encode<little>(const ArraypadCounterAligns_Helper& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounterAligns_Helper>::encode<big>(const ArraypadCounterAligns_Helper& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<ArraypadCounterAligns>::encode(const ArraypadCounterAligns& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = pos + 1;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<ArraypadCounterAligns>::encode<native>(const ArraypadCounterAligns& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounterAligns>::encode<little>(const ArraypadCounterAligns& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadCounterAligns>::encode<big>(const ArraypadCounterAligns& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<ArraypadFixed>::encode(const ArraypadFixed& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x);
    pos = do_encode<E>(pos, x.y, 3);
    pos = pos + 1;
    pos = do_encode<E>(pos, x.z);
    return pos;
}
template uint8_t* message_impl<ArraypadFixed>::encode<native>(const ArraypadFixed& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadFixed>::encode<little>(const ArraypadFixed& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadFixed>::encode<big>(const ArraypadFixed& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<ArraypadDynamic>::encode(const ArraypadDynamic& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    pos = align<4>(pos);
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<ArraypadDynamic>::encode<native>(const ArraypadDynamic& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadDynamic>::encode<little>(const ArraypadDynamic& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadDynamic>::encode<big>(const ArraypadDynamic& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<ArraypadLimited>::encode(const ArraypadLimited& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(2))));
    do_encode<E>(pos, x.x.data(), std::min(x.x.size(), size_t(2)));
    pos = pos + 2;
    pos = pos + 2;
    pos = do_encode<E>(pos, x.y);
    return pos;
}
template uint8_t* message_impl<ArraypadLimited>::encode<native>(const ArraypadLimited& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadLimited>::encode<little>(const ArraypadLimited& x, uint8_t* pos);
template uint8_t* message_impl<ArraypadLimited>::encode<big>(const ArraypadLimited& x, uint8_t* pos);

} // namespace detail
} // namespace prophy
