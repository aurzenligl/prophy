#ifndef _PROPHY_DETAIL_DECODER_HPP_
#define _PROPHY_DETAIL_DECODER_HPP_

#include <stdint.h>
#include <prophy/endianness.hpp>
#include <prophy/detail/codec_traits.hpp>
#include <prophy/detail/decode_composite.hpp>

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
        if (size_t(end - pos) >= sizeof(T))
        {
            decode_int<E>(x, pos);
            pos += sizeof(T);
            return true;
        }
        return false;
    }
};

template <endianness E, typename T>
inline bool do_decode(T& x, const uint8_t*& pos, const uint8_t* end)
{
    return decoder<E, T>::decode(x, pos, end);
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_DECODER_HPP_ */
