#ifndef _PROPHY_DETAIL_DECODE_COMPOSITE_HPP_
#define _PROPHY_DETAIL_DECODE_COMPOSITE_HPP_

#include <stdint.h>
#include <prophy/endianness.hpp>
#include <prophy/detail/codec_traits.hpp>

namespace prophy
{
namespace detail
{

template <typename T>
struct decode_composite
{
    template <endianness E>
    static bool decode(T& x, const uint8_t*& pos, const uint8_t* end);
};

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_DECODE_COMPOSITE_HPP_ */
