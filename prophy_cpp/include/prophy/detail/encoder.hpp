#ifndef _PROPHY_DETAIL_ENCODER_HPP_
#define _PROPHY_DETAIL_ENCODER_HPP_

#include <stdint.h>
#include <prophy/endianness.hpp>
#include <prophy/detail/codec_traits.hpp>

namespace prophy
{
namespace detail
{

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

template <typename T>
struct number_encoder<little, T>
{
    static void encode(void* data, const T& x)
    {
        *static_cast<T*>(data) = x;
    }
};

template <typename T>
struct number_encoder<big, T>
{
    static void encode(void* data, const T& x)
    {
        *static_cast<T*>(data) = x;
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
uint8_t* do_encode(uint8_t* data, const T& x)
{
    return encoder<E, T>::encode(data, x);
}

template <endianness E, typename T>
uint8_t* do_encode(uint8_t* data, const T* x, size_t n)
{
    return encoder<E, T>::encode(data, x, n);
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_ENCODER_HPP_ */
