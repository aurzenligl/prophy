#ifndef _PROPHY_DETAIL_DECODER_HPP_
#define _PROPHY_DETAIL_DECODER_HPP_

#include <stdint.h>
#include <prophy/endianness.hpp>
#include <prophy/detail/codec_traits.hpp>
#include <prophy/detail/message_impl.hpp>

namespace prophy
{
namespace detail
{

template <endianness E, typename T>
inline void decode_int(T& x, const uint8_t* pos)
{
    x = *reinterpret_cast<const T*>(pos);
}

template <endianness E, typename T,
          bool = codec_traits<T>::is_composite,
          bool = codec_traits<T>::size == -1>
struct decoder;

template <endianness E, typename T>
struct decoder<E, T, false, false>
{
    static bool decode(T& x, const uint8_t*& pos, const uint8_t* end)
    {
        if (size_t(end - pos) < sizeof(T))
        {
            return false;
        }
        decode_int<E>(x, pos);
        pos += sizeof(T);
        return true;
    }

    static bool decode(T* x, size_t n, const uint8_t*& pos, const uint8_t* end)
    {
        if (size_t(end - pos) < n * sizeof(T))
        {
            return false;
        }
        while (n)
        {
            decode_int<E>(*x, pos);
            pos += sizeof(T);
            ++x;
            --n;
        }
        return true;
    }
};

template <endianness E, typename T>
inline bool do_decode(T& x, const uint8_t*& pos, const uint8_t* end)
{
    return decoder<E, T>::decode(x, pos, end);
}

template <endianness E, typename T>
inline bool do_decode(T* x, size_t n, const uint8_t*& pos, const uint8_t* end)
{
    return decoder<E, T>::decode(x, n, pos, end);
}

template <endianness E, typename T, class V>
inline bool do_decode_resize(V& v, const uint8_t*& pos, const uint8_t* end)
{
    T x;
    if (!decoder<E, T>::decode(x, pos, end))
    {
        return false;
    }
    v.resize(x);
    return true;
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_DECODER_HPP_ */
