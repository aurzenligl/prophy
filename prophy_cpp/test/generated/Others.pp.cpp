#include "Others.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t ConstantTypedefEnum::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, a, 3);
    pos = do_encode<E>(pos, b);
    pos = do_encode<E>(pos, uint32_t(c));
    return pos - static_cast<uint8_t*>(data);
}

template size_t ConstantTypedefEnum::encode<native>(void* data) const;

template <endianness E>
size_t BytesFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x, 3);
    return pos - static_cast<uint8_t*>(data);
}

template size_t BytesFixed::encode<native>(void* data) const;

template <endianness E>
size_t BytesDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), uint32_t(x.size()));
    pos = align<4>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t BytesDynamic::encode<native>(void* data) const;

template <endianness E>
size_t BytesLimited::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(std::min(x.size(), size_t(4))));
    do_encode<E>(pos, x.data(), std::min(x.size(), size_t(4)));
    pos = pos + 4;
    return pos - static_cast<uint8_t*>(data);
}

template size_t BytesLimited::encode<native>(void* data) const;

template <endianness E>
size_t BytesGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t BytesGreedy::encode<native>(void* data) const;
