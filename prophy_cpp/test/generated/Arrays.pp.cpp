#include "Arrays.pp.hpp"
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t Builtin::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    const uint8_t* begin = pos;
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y);
    return pos - begin;
}

template size_t Builtin::encode<native>(void* data) const;
