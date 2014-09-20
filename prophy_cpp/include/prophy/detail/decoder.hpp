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
struct decoder<E, T, true, false>
{
    static bool decode(T& x, const uint8_t*& pos, const uint8_t* end)
    {
        return message_impl<T>::template decode<E>(x, pos, end);
    }

    static bool decode(T* x, size_t n, const uint8_t*& pos, const uint8_t* end)
    {
        while (n)
        {
            if (!message_impl<T>::template decode<E>(*x, pos, end))
            {
                return false;
            }
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

template <endianness E, typename T>
inline bool do_decode_in_place(T* x, size_t n, const uint8_t* pos, const uint8_t* end)
{
    return decoder<E, T>::decode(x, n, pos, end);
}

template <endianness E, typename T>
inline bool do_decode_greedy(std::vector<T>& v, const uint8_t*& pos, const uint8_t* end)
{
    size_t n = size_t(end - pos) / sizeof(T);
    size_t mod = size_t(end - pos) % sizeof(T);
    if (mod)
    {
        return false;
    }
    v.resize(n);
    return decoder<E, T>::decode(v.data(), n, pos, end);
}

template <endianness E, typename CT, typename T>
inline bool do_decode_resize(std::vector<T>& v, const uint8_t*& pos, const uint8_t* end, size_t max = ~size_t())
{
    CT n;
    if (!decoder<E, CT>::decode(n, pos, end))
    {
        return false;
    }
    if (n > max)
    {
        return false;
    }
    v.resize(n);
    return true;
}

inline bool do_decode_advance(size_t n, const uint8_t*& pos, const uint8_t* end)
{
    if (size_t(end - pos) < n)
    {
        return false;
    }
    pos += n;
    return true;
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_DECODER_HPP_ */
