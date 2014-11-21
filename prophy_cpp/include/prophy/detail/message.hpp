#ifndef _PROPHY_DETAIL_MESSAGE_HPP_
#define _PROPHY_DETAIL_MESSAGE_HPP_

#include <stddef.h>
#include <stdint.h>
#include <string>
#include <vector>
#include <sstream>
#include <prophy/endianness.hpp>
#include <prophy/detail/message_impl.hpp>

namespace prophy
{
namespace detail
{

template <class T>
struct message
{
    template <endianness E>
    size_t encode(void* data) const
    {
        uint8_t* pos = static_cast<uint8_t*>(data);
        uint8_t* end = message_impl<T>::template encode<E>(*static_cast<const T*>(this), pos);
        return end - pos;
    }

    size_t encode(void* data) const
    {
        return encode<native>(data);
    }

    template <endianness E>
    std::vector<uint8_t> encode() const
    {
        std::vector<uint8_t> data(static_cast<const T*>(this)->get_byte_size());
        message_impl<T>::template encode<E>(*static_cast<const T*>(this), data.data());
        return data;
    }

    std::vector<uint8_t> encode() const
    {
        return encode<native>();
    }

    template <endianness E>
    bool decode(const void* data, size_t size)
    {
        const uint8_t* data_ = static_cast<const uint8_t*>(data);
        bool success = message_impl<T>::template decode<E>(*static_cast<T*>(this), data_, data_ + size);
        size_t bytes_read = data_ - static_cast<const uint8_t*>(data);
        return success && (bytes_read == size);
    }

    bool decode(const void* data, size_t size)
    {
        return decode<native>(data, size);
    }

    template <endianness E>
    bool decode(const std::vector<uint8_t>& data)
    {
        return decode<E>(data.data(), data.size());
    }

    bool decode(const std::vector<uint8_t>& data)
    {
        return decode<native>(data);
    }

    std::string print() const
    {
        std::stringstream ss;
        message_impl<T>::print(*static_cast<const T*>(this), ss, 0);
        return ss.str();
    }
};

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_MESSAGE_HPP_ */
