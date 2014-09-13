#ifndef _PROPHY_GENERATED_Paddings_HPP
#define _PROPHY_GENERATED_Paddings_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/endianness.hpp>

struct Endpad
{
    enum { encoded_byte_size = 4 };

    uint16_t x;
    uint8_t y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct EndpadFixed
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint8_t y[3];

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct EndpadDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct EndpadLimited
{
    enum { encoded_byte_size = 8 };

    std::vector<uint8_t> x; /// limit 2

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct EndpadGreedy
{
    enum { encoded_byte_size = -1 };

    uint32_t x;
    std::vector<uint8_t> y; /// greedy

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Paddings_HPP */
