#ifndef _PROPHY_GENERATED_Array_HPP
#define _PROPHY_GENERATED_Array_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/endianness.hpp>

struct Builtin
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint32_t y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinFixed
{
    enum { encoded_byte_size = 8 };

    uint32_t x[2];

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinLimited
{
    enum { encoded_byte_size = 12 };

    std::vector<uint32_t> x; /// limit 2

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x; /// greedy

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Array_HPP */
