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
