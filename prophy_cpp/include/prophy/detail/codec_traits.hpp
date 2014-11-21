#ifndef _PROPHY_DETAIL_CODEC_TRAITS_HPP_
#define _PROPHY_DETAIL_CODEC_TRAITS_HPP_

#include <stdint.h>
#include <prophy/detail/mpl.hpp>

namespace prophy
{
namespace detail
{

template <typename T, bool IsClass = is_class_or_union<T>::value>
struct codec_traits;

template <typename T>
struct codec_traits<T, true>
{
    enum { is_composite = true };
    enum { is_enum_or_bool = false };
    enum { size = T::encoded_byte_size };
};

template <>
struct codec_traits<int8_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 1 };
};

template <>
struct codec_traits<int16_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 2 };
};

template <>
struct codec_traits<int32_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 4 };
};

template <>
struct codec_traits<int64_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 8 };
};

template <>
struct codec_traits<uint8_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 1 };
};

template <>
struct codec_traits<uint16_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 2 };
};

template <>
struct codec_traits<uint32_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 4 };
};

template <>
struct codec_traits<uint64_t, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 8 };
};

template <>
struct codec_traits<float, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 4 };
};

template <>
struct codec_traits<double, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = 8 };
};

/// enum or bool
template <typename T>
struct codec_traits<T, false>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = true };
    enum { size = sizeof(uint32_t) };
};

/// bytes
template <>
struct codec_traits<std::pair<const uint8_t*, size_t>, true>
{
    enum { is_composite = false };
    enum { is_enum_or_bool = false };
    enum { size = -1 };
};

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_CODEC_TRAITS_HPP_ */
