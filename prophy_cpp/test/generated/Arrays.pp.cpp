#include "Arrays.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t Builtin::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Builtin::encode<native>(void* data) const;

template <endianness E>
size_t BuiltinFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x, 2);
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinFixed::encode<native>(void* data) const;

template <endianness E>
size_t BuiltinDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinDynamic::encode<native>(void* data) const;

template <endianness E>
size_t BuiltinLimited::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(std::min(x.size(), size_t(2))));
    do_encode<E>(pos, x.data(), std::min(x.size(), size_t(2)));
    pos = pos + 8;
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinLimited::encode<native>(void* data) const;

template <endianness E>
size_t BuiltinGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinGreedy::encode<native>(void* data) const;
