#ifndef _PROPHY_DETAIL_ENCODER_HPP_
#define _PROPHY_DETAIL_ENCODER_HPP_

#include <stdint.h>
#include <prophy/endianness.hpp>
#include <prophy/optional.hpp>
#include <prophy/detail/codec_traits.hpp>
#include <prophy/detail/message_impl.hpp>
#include <prophy/detail/align.hpp>

namespace prophy
{
namespace detail
{

template <endianness E, typename T>
inline void encode_int(uint8_t* out, const T& in)
{
    *reinterpret_cast<T*>(out) = in;
}

template <>
inline void encode_int<little, uint16_t>(uint8_t* out, const uint16_t& in)
{
    out[0] = (in & 0x00FF) >> 0;
    out[1] = (in & 0xFF00) >> 8;
}

template <>
inline void encode_int<big, uint16_t>(uint8_t* out, const uint16_t& in)
{
    out[0] = (in & 0xFF00) >> 8;
    out[1] = (in & 0x00FF) >> 0;
}

template <>
inline void encode_int<little, int16_t>(uint8_t* out, const int16_t& in)
{
    encode_int<little>(out, static_cast<const uint16_t&>(in));
}

template <>
inline void encode_int<big, int16_t>(uint8_t* out, const int16_t& in)
{
    encode_int<big>(out, static_cast<const uint16_t&>(in));
}

template <>
inline void encode_int<little, uint32_t>(uint8_t* out, const uint32_t& in)
{
    out[0] = (in & 0x000000FF) >> 0;
    out[1] = (in & 0x0000FF00) >> 8;
    out[2] = (in & 0x00FF0000) >> 16;
    out[3] = (in & 0xFF000000) >> 24;
}

template <>
inline void encode_int<big, uint32_t>(uint8_t* out, const uint32_t& in)
{
    out[0] = (in & 0xFF000000) >> 24;
    out[1] = (in & 0x00FF0000) >> 16;
    out[2] = (in & 0x0000FF00) >> 8;
    out[3] = (in & 0x000000FF) >> 0;
}

template <>
inline void encode_int<little, int32_t>(uint8_t* out, const int32_t& in)
{
    encode_int<little>(out, static_cast<const uint32_t&>(in));
}

template <>
inline void encode_int<big, int32_t>(uint8_t* out, const int32_t& in)
{
    encode_int<big>(out, static_cast<const uint32_t&>(in));
}

template <>
inline void encode_int<little, uint64_t>(uint8_t* out, const uint64_t& in)
{
    out[0] = (in & 0x00000000000000FFULL) >> 0;
    out[1] = (in & 0x000000000000FF00ULL) >> 8;
    out[2] = (in & 0x0000000000FF0000ULL) >> 16;
    out[3] = (in & 0x00000000FF000000ULL) >> 24;
    out[4] = (in & 0x000000FF00000000ULL) >> 32;
    out[5] = (in & 0x0000FF0000000000ULL) >> 40;
    out[6] = (in & 0x00FF000000000000ULL) >> 48;
    out[7] = (in & 0xFF00000000000000ULL) >> 56;
}

template <>
inline void encode_int<big, uint64_t>(uint8_t* out, const uint64_t& in)
{
    out[0] = (in & 0xFF00000000000000ULL) >> 56;
    out[1] = (in & 0x00FF000000000000ULL) >> 48;
    out[2] = (in & 0x0000FF0000000000ULL) >> 40;
    out[3] = (in & 0x000000FF00000000ULL) >> 32;
    out[4] = (in & 0x00000000FF000000ULL) >> 24;
    out[5] = (in & 0x0000000000FF0000ULL) >> 16;
    out[6] = (in & 0x000000000000FF00ULL) >> 8;
    out[7] = (in & 0x00000000000000FFULL) >> 0;
}

template <>
inline void encode_int<little, int64_t>(uint8_t* out, const int64_t& in)
{
    encode_int<little>(out, static_cast<const uint64_t&>(in));
}

template <>
inline void encode_int<big, int64_t>(uint8_t* out, const int64_t& in)
{
    encode_int<big>(out, static_cast<const uint64_t&>(in));
}

template <>
inline void encode_int<little, float>(uint8_t* out, const float& in)
{
    encode_int<little>(out, reinterpret_cast<const uint32_t&>(in));
}

template <>
inline void encode_int<big, float>(uint8_t* out, const float& in)
{
    encode_int<big>(out, reinterpret_cast<const uint32_t&>(in));
}

template <>
inline void encode_int<little, double>(uint8_t* out, const double& in)
{
    encode_int<little>(out, reinterpret_cast<const uint64_t&>(in));
}

template <>
inline void encode_int<big, double>(uint8_t* out, const double& in)
{
    encode_int<big>(out, reinterpret_cast<const uint64_t&>(in));
}

template <endianness E, typename T,
          bool = codec_traits<T>::is_composite,
          bool = codec_traits<T>::is_enum_or_bool,
          bool = codec_traits<T>::size == -1>
struct encoder;

template <endianness E, typename T>
struct encoder<E, T, false, false, false>
{
    static uint8_t* encode(uint8_t* data, const T& x)
    {
        encode_int<E>(data, x);
        return data + sizeof(T);
    }
    static uint8_t* encode(uint8_t* data, const T* x, size_t n)
    {
        while (n)
        {
            encode_int<E>(data, *x);
            data += sizeof(T);
            ++x;
            --n;
        }
        return data;
    }
};

template <endianness E, typename T>
struct encoder<E, T, false, true, false>
{
    static uint8_t* encode(uint8_t* data, const T& x)
    {
        encode_int<E>(data, uint32_t(x));
        return data + sizeof(uint32_t);
    }
    static uint8_t* encode(uint8_t* data, const T* x, size_t n)
    {
        while (n)
        {
            encode_int<E>(data, uint32_t(*x));
            data += sizeof(uint32_t);
            ++x;
            --n;
        }
        return data;
    }
};

template <endianness E, typename T>
struct encoder<E, T, true, false, false>
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
struct encoder<E, T, true, false, true>
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

template <endianness E, typename T>
inline uint8_t* do_encode(uint8_t* data, const optional<T>& x)
{
    data = do_encode<E>(data, uint32_t(bool(x)));
    if (alignment<T>::value > sizeof(uint32_t))
    {
        data = data + alignment<T>::value - sizeof(uint32_t);
    }
    if (x)
    {
        return do_encode<E>(data, *x);
    }
    return data + codec_traits<T>::size;
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_ENCODER_HPP_ */
