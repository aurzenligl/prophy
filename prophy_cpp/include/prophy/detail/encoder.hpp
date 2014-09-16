#ifndef _PROPHY_DETAIL_ENCODER_HPP_
#define _PROPHY_DETAIL_ENCODER_HPP_

#include <stdint.h>
#include <prophy/endianness.hpp>
#include <prophy/detail/codec_traits.hpp>

namespace prophy
{
namespace detail
{

inline void encode_little_int(uint8_t* out, const uint16_t& in)
{
    out[0] = (in & 0x00FF) >> 0;
    out[1] = (in & 0xFF00) >> 8;
}

inline void encode_big_int(uint8_t* out, const uint16_t& in)
{
    out[0] = (in & 0xFF00) >> 8;
    out[1] = (in & 0x00FF) >> 0;
}

inline void encode_little_int(uint8_t* out, const uint32_t& in)
{
    out[0] = (in & 0x000000FF) >> 0;
    out[1] = (in & 0x0000FF00) >> 8;
    out[2] = (in & 0x00FF0000) >> 16;
    out[3] = (in & 0xFF000000) >> 24;
}

inline void encode_big_int(uint8_t* out, const uint32_t& in)
{
    out[0] = (in & 0xFF000000) >> 24;
    out[1] = (in & 0x00FF0000) >> 16;
    out[2] = (in & 0x0000FF00) >> 8;
    out[3] = (in & 0x000000FF) >> 0;
}

template <endianness E, typename T>
struct number_encoder;

template <typename T>
struct number_encoder<native, T>
{
    static void encode(void* data, const T& x)
    {
        *static_cast<T*>(data) = x;
    }
};

template <>
struct number_encoder<little, int16_t>
{
    static void encode(void* data, const uint16_t& x)
    {
        encode_little_int(static_cast<uint8_t*>(data), x);
    }
};

template <>
struct number_encoder<little, uint16_t>
{
    static void encode(void* data, const int16_t& x)
    {
        encode_little_int(static_cast<uint8_t*>(data), static_cast<const uint16_t&>(x));
    }
};

template <>
struct number_encoder<little, int32_t>
{
    static void encode(void* data, const uint32_t& x)
    {
        encode_little_int(static_cast<uint8_t*>(data), x);
    }
};

template <>
struct number_encoder<little, uint32_t>
{
    static void encode(void* data, const int32_t& x)
    {
        encode_little_int(static_cast<uint8_t*>(data), static_cast<const uint32_t&>(x));
    }
};

template <>
struct number_encoder<big, int16_t>
{
    static void encode(void* data, const int16_t& x)
    {
        encode_big_int(static_cast<uint8_t*>(data), static_cast<const uint16_t&>(x));
    }
};

template <>
struct number_encoder<big, uint16_t>
{
    static void encode(void* data, const uint16_t& x)
    {
        encode_big_int(static_cast<uint8_t*>(data), x);
    }
};

template <>
struct number_encoder<big, int32_t>
{
    static void encode(void* data, const int32_t& x)
    {
        encode_big_int(static_cast<uint8_t*>(data), static_cast<const uint32_t&>(x));
    }
};

template <>
struct number_encoder<big, uint32_t>
{
    static void encode(void* data, const uint32_t& x)
    {
        encode_big_int(static_cast<uint8_t*>(data), x);
    }
};

template <endianness E, typename T,
          bool = codec_traits<T>::is_composite,
          bool = codec_traits<T>::size == -1>
struct encoder;

template <endianness E, typename T>
struct encoder<E, T, false, false>
{
    static uint8_t* encode(uint8_t* data, const T& x)
    {
        number_encoder<E, T>::encode(data, x);
        return data + sizeof(T);
    }
    static uint8_t* encode(uint8_t* data, const T* x, size_t n)
    {
        while (n)
        {
            number_encoder<E, T>::encode(data, *x);
            data += sizeof(T);
            ++x;
            --n;
        }
        return data;
    }
};

template <endianness E, typename T>
struct encoder<E, T, true, false>
{
    static uint8_t* encode(uint8_t* data, const T& x)
    {
        x.template encode<E>(data);
        return data + T::encoded_byte_size;
    }
    static uint8_t* encode(uint8_t* data, const T* x, size_t n)
    {
        while (n)
        {
            x->template encode<E>(data);
            data += T::encoded_byte_size;
            ++x;
            --n;
        }
        return data;
    }
};

template <endianness E, typename T>
struct encoder<E, T, true, true>
{
    static uint8_t* encode(uint8_t* data, const T& x)
    {
        return data + x.template encode<E>(data);
    }
    static uint8_t* encode(uint8_t* data, const T* x, size_t n)
    {
        while (n)
        {
            data += x->template encode<E>(data);
            ++x;
            --n;
        }
        return data;
    }
};

template <endianness E, typename T>
inline uint8_t* do_encode(uint8_t* data, const T& x)
{
    return encoder<E, T>::encode(data, x);
}

template <endianness E, typename T>
inline uint8_t* do_encode(uint8_t* data, const T* x, size_t n)
{
    return encoder<E, T>::encode(data, x, n);
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_ENCODER_HPP_ */
