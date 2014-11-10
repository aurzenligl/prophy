#ifndef _PROPHY_DETAIL_DECODER_HPP_
#define _PROPHY_DETAIL_DECODER_HPP_

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
inline void decode_int(T& x, const uint8_t* pos)
{
    x = *reinterpret_cast<const T*>(pos);
}

template <>
inline void decode_int<little, uint16_t>(uint16_t& x, const uint8_t* pos)
{
    x = uint16_t(pos[0]) << 0;
    x |= uint16_t(pos[1]) << 8;
}

template <>
inline void decode_int<big, uint16_t>(uint16_t& x, const uint8_t* pos)
{
    x = uint16_t(pos[0]) << 8;
    x |= uint16_t(pos[1]) << 0;
}

template <>
inline void decode_int<little, int16_t>(int16_t& x, const uint8_t* pos)
{
    decode_int<little>(reinterpret_cast<uint16_t&>(x), pos);
}

template <>
inline void decode_int<big, int16_t>(int16_t& x, const uint8_t* pos)
{
    decode_int<big>(reinterpret_cast<uint16_t&>(x), pos);
}

template <>
inline void decode_int<little, uint32_t>(uint32_t& x, const uint8_t* pos)
{
    x = uint32_t(pos[0]) << 0;
    x |= uint32_t(pos[1]) << 8;
    x |= uint32_t(pos[2]) << 16;
    x |= uint32_t(pos[3]) << 24;
}

template <>
inline void decode_int<big, uint32_t>(uint32_t& x, const uint8_t* pos)
{
    x = uint32_t(pos[0]) << 24;
    x |= uint32_t(pos[1]) << 16;
    x |= uint32_t(pos[2]) << 8;
    x |= uint32_t(pos[3]) << 0;
}

template <>
inline void decode_int<little, int32_t>(int32_t& x, const uint8_t* pos)
{
    decode_int<little>(reinterpret_cast<uint32_t&>(x), pos);
}

template <>
inline void decode_int<big, int32_t>(int32_t& x, const uint8_t* pos)
{
    decode_int<big>(reinterpret_cast<uint32_t&>(x), pos);
}

template <>
inline void decode_int<little, uint64_t>(uint64_t& x, const uint8_t* pos)
{
    x = uint64_t(pos[0]) << 0;
    x |= uint64_t(pos[1]) << 8;
    x |= uint64_t(pos[2]) << 16;
    x |= uint64_t(pos[3]) << 24;
    x |= uint64_t(pos[4]) << 32;
    x |= uint64_t(pos[5]) << 40;
    x |= uint64_t(pos[6]) << 48;
    x |= uint64_t(pos[7]) << 56;
}

template <>
inline void decode_int<big, uint64_t>(uint64_t& x, const uint8_t* pos)
{
    x = uint64_t(pos[0]) << 56;
    x |= uint64_t(pos[1]) << 48;
    x |= uint64_t(pos[2]) << 40;
    x |= uint64_t(pos[3]) << 32;
    x |= uint64_t(pos[4]) << 24;
    x |= uint64_t(pos[5]) << 16;
    x |= uint64_t(pos[6]) << 8;
    x |= uint64_t(pos[7]) << 0;
}

template <>
inline void decode_int<little, int64_t>(int64_t& x, const uint8_t* pos)
{
    decode_int<little>(reinterpret_cast<uint64_t&>(x), pos);
}

template <>
inline void decode_int<big, int64_t>(int64_t& x, const uint8_t* pos)
{
    decode_int<big>(reinterpret_cast<uint64_t&>(x), pos);
}

template <>
inline void decode_int<little, float>(float& x, const uint8_t* pos)
{
    decode_int<little>(reinterpret_cast<uint32_t&>(x), pos);
}

template <>
inline void decode_int<big, float>(float& x, const uint8_t* pos)
{
    decode_int<big>(reinterpret_cast<uint32_t&>(x), pos);
}

template <>
inline void decode_int<little, double>(double& x, const uint8_t* pos)
{
    decode_int<little>(reinterpret_cast<uint64_t&>(x), pos);
}

template <>
inline void decode_int<big, double>(double& x, const uint8_t* pos)
{
    decode_int<big>(reinterpret_cast<uint64_t&>(x), pos);
}

template <endianness E, typename T,
          bool = codec_traits<T>::is_composite,
          bool = codec_traits<T>::is_enum_or_bool,
          bool = codec_traits<T>::size == -1>
struct decoder;

template <endianness E, typename T>
struct decoder<E, T, false, false, false>
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
struct decoder<E, T, false, true, false>
{
    static bool decode(T& x, const uint8_t*& pos, const uint8_t* end)
    {
        if (size_t(end - pos) < sizeof(uint32_t))
        {
            return false;
        }
        uint32_t data;
        decode_int<E>(data, pos);
        x = static_cast<T>(data);
        pos += sizeof(uint32_t);
        return true;
    }

    static bool decode(T* x, size_t n, const uint8_t*& pos, const uint8_t* end)
    {
        if (size_t(end - pos) < n * sizeof(uint32_t))
        {
            return false;
        }
        while (n)
        {
            uint32_t data;
            decode_int<E>(data, pos);
            *x = static_cast<T>(data);
            pos += sizeof(uint32_t);
            ++x;
            --n;
        }
        return true;
    }
};

template <endianness E, typename T>
struct decoder<E, T, true, false, false>
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
struct decoder<E, T, true, false, true>
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

template <endianness E, typename T,
          bool = codec_traits<T>::size == -1>
struct decoder_greedy;

template <endianness E, typename T>
struct decoder_greedy<E, T, false>
{
    static bool decode(std::vector<T>& v, const uint8_t*& pos, const uint8_t* end)
    {
        size_t n = size_t(end - pos) / codec_traits<T>::size;
        v.resize(n);
        return decoder<E, T>::decode(v.data(), n, pos, end);
    }
};

template <endianness E, typename T>
struct decoder_greedy<E, T, true>
{
    static bool decode(std::vector<T>& v, const uint8_t*& pos, const uint8_t* end)
    {
        v.resize(0);
        while(true)
        {
            v.push_back(T());
            if (!decoder<E, T>::decode(v.back(), pos, end))
            {
                v.pop_back();
                return true;
            }
        }
    }
};

inline bool do_decode_advance(size_t n, const uint8_t*& pos, const uint8_t* end)
{
    if (size_t(end - pos) < n)
    {
        return false;
    }
    pos += n;
    return true;
}

template <size_t A>
inline bool do_decode_align(const uint8_t*& pos, const uint8_t* end)
{
    const uint8_t* aligned = align<A>(pos);
    if (aligned > end)
    {
        return false;
    }
    pos = aligned;
    return true;
}

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
inline bool do_decode(optional<T>& x, const uint8_t*& pos, const uint8_t* end)
{
    uint32_t disc;
    if (!do_decode<E>(disc, pos, end))
    {
        return false;
    }
    x = disc ? optional<T>(T()) : optional<T>();
    if (alignment<T>::value > sizeof(uint32_t))
    {
        if (!do_decode_advance(alignment<T>::value - sizeof(uint32_t), pos, end))
        {
            return false;
        }
    }
    if (disc)
    {
        return decoder<E, T>::decode(*x, pos, end);
    }
    pos = pos + codec_traits<T>::size;
    return true;
}

template <endianness E, typename T>
inline bool do_decode_in_place(T& x, const uint8_t* pos, const uint8_t* end)
{
    return decoder<E, T>::decode(x, pos, end);
}

template <endianness E, typename T>
inline bool do_decode_in_place(T* x, size_t n, const uint8_t* pos, const uint8_t* end)
{
    return decoder<E, T>::decode(x, n, pos, end);
}

template <endianness E, typename T>
inline bool do_decode_greedy(std::vector<T>& v, const uint8_t*& pos, const uint8_t* end)
{
    return decoder_greedy<E, T>::decode(v, pos, end);
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

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_DECODER_HPP_ */
