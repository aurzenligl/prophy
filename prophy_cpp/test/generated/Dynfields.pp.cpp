#include "Dynfields.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t Dynfields::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), uint32_t(x.size()));
    pos = align<2>(pos);
    pos = do_encode<E>(pos, uint16_t(y.size()));
    pos = do_encode<E>(pos, y.data(), uint16_t(y.size()));
    pos = align<8>(pos);
    pos = do_encode<E>(pos, z);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Dynfields::encode<native>(void* data) const;

template <endianness E>
size_t DynfieldsMixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, uint16_t(y.size()));
    pos = do_encode<E>(pos, x.data(), uint32_t(x.size()));
    pos = align<2>(pos);
    pos = do_encode<E>(pos, y.data(), uint16_t(y.size()));
    pos = align<4>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t DynfieldsMixed::encode<native>(void* data) const;

template <endianness E>
size_t DynfieldsOverlapped::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(a.size()));
    pos = do_encode<E>(pos, uint32_t(b.size()));
    pos = do_encode<E>(pos, b.data(), uint32_t(b.size()));
    pos = align<4>(pos);
    pos = do_encode<E>(pos, uint32_t(c.size()));
    pos = do_encode<E>(pos, c.data(), uint32_t(c.size()));
    pos = do_encode<E>(pos, a.data(), uint32_t(a.size()));
    pos = align<4>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t DynfieldsOverlapped::encode<native>(void* data) const;
