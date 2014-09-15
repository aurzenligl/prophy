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
