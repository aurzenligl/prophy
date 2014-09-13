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

struct Scalarpad
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    uint16_t y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppre_Helper
{
    enum { encoded_byte_size = 1 };

    uint8_t x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppre
{
    enum { encoded_byte_size = 4 };

    ScalarpadComppre_Helper x;
    uint16_t y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppost_Helper
{
    enum { encoded_byte_size = 2 };

    uint16_t x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppost
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    ScalarpadComppost_Helper y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadOptionalboolpad
{
    enum { encoded_byte_size = 12 };

    uint8_t x;
    bool has_y;
    uint8_t y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadOptionalvaluepad
{
    enum { encoded_byte_size = 16 };

    bool has_x;
    uint64_t x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadDiscpad_Helper
{
    enum { encoded_byte_size = 8 };

    enum _discriminator
    {
        discriminator_a = 1
    } discriminator;

    union
    {
        uint8_t a;
    };

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadDiscpad
{
    enum { encoded_byte_size = 16 };

    uint8_t x;
    UnionpadDiscpad_Helper y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadArmpad_Helper
{
    enum { encoded_byte_size = 16 };

    enum _discriminator
    {
        discriminator_a = 1,
        discriminator_b = 2
    } discriminator;

    union
    {
        uint8_t a;
        uint64_t b;
    };

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadArmpad
{
    enum { encoded_byte_size = 24 };

    uint8_t x;
    UnionpadArmpad_Helper y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Paddings_HPP */
