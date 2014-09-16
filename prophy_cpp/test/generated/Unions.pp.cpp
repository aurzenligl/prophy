#include "Unions.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t Union::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(discriminator));
    switch(discriminator)
    {
        case discriminator_a: do_encode<E>(pos, a); break;
        case discriminator_b: do_encode<E>(pos, b); break;
        case discriminator_c: do_encode<E>(pos, c); break;
    }
    pos = pos + 8;
    return pos - static_cast<uint8_t*>(data);
}

template size_t Union::encode<native>(void* data) const;
template size_t Union::encode<little>(void* data) const;
template size_t Union::encode<big>(void* data) const;

template <endianness E>
size_t BuiltinOptional::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(has_x));
    if (has_x) do_encode<E>(pos, x);
    pos = pos + 4;
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinOptional::encode<native>(void* data) const;
template size_t BuiltinOptional::encode<little>(void* data) const;
template size_t BuiltinOptional::encode<big>(void* data) const;

template <endianness E>
size_t FixcompOptional::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(has_x));
    if (has_x) do_encode<E>(pos, x);
    pos = pos + 8;
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompOptional::encode<native>(void* data) const;
template size_t FixcompOptional::encode<little>(void* data) const;
template size_t FixcompOptional::encode<big>(void* data) const;
