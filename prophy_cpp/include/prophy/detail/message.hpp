#ifndef _PROPHY_DETAIL_MESSAGE_HPP_
#define _PROPHY_DETAIL_MESSAGE_HPP_

#include <stdint.h>
#include <stddef.h>
#include <prophy/endianness.hpp>

namespace prophy
{
namespace detail
{

template <class T>
struct message
{
    template <prophy::endianness E>
    size_t encode(void* data) const
    {
        return static_cast<const T*>(this)->template encode_impl<E>(data);
    }

    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }

    template <prophy::endianness E>
    bool decode(const void* data, size_t size)
    {
        const uint8_t* data_ = static_cast<const uint8_t*>(data);
        bool success = static_cast<T*>(this)->template decode_impl<E>(data_, data_ + size);
        size_t bytes_read = data_ - static_cast<const uint8_t*>(data);
        return success && (bytes_read == size);
    }

    bool decode(const void* data, size_t size)
    {
        return decode<prophy::native>(data, size);
    }
};

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_MESSAGE_HPP_ */
