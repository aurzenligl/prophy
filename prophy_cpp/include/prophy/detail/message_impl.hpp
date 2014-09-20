#ifndef _PROPHY_DETAIL_MESSAGE_IMPL_HPP_
#define _PROPHY_DETAIL_MESSAGE_IMPL_HPP_

#include <stdint.h>
#include <prophy/endianness.hpp>

namespace prophy
{
namespace detail
{

template <typename T>
struct message_impl
{
    template <endianness E>
    static uint8_t* encode(const T& x, uint8_t* pos);

    template <endianness E>
    static bool decode(T& x, const uint8_t*& pos, const uint8_t* end);
};

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_MESSAGE_IMPL_HPP_ */
