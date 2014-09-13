#include "Paddings.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t Endpad::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y);
    pos = pos + 1;
    return pos - static_cast<uint8_t*>(data);
}

template size_t Endpad::encode<native>(void* data) const;

template <endianness E>
size_t EndpadFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y, 3);
    pos = pos + 1;
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadFixed::encode<native>(void* data) const;

template <endianness E>
size_t EndpadDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    pos = align<4>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadDynamic::encode<native>(void* data) const;

template <endianness E>
size_t EndpadLimited::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(std::min(x.size(), size_t(2))));
    do_encode<E>(pos, x.data(), std::min(x.size(), size_t(2)));
    pos = pos + 4;
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadLimited::encode<native>(void* data) const;

template <endianness E>
size_t EndpadGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x));
    pos = do_encode<E>(pos, y.data(), y.size());
    pos = align<4>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadGreedy::encode<native>(void* data) const;
