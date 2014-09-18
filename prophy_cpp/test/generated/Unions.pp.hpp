#ifndef _PROPHY_GENERATED_Unions_HPP
#define _PROPHY_GENERATED_Unions_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>

#include "Arrays.pp.hpp"

struct Union
{
    enum { encoded_byte_size = 12 };

    enum _discriminator
    {
        discriminator_a = 1,
        discriminator_b = 2,
        discriminator_c = 3
    } discriminator;

    uint8_t a;
    uint32_t b;
    Builtin c;

    Union(): discriminator(discriminator_a), a(), b() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinOptional
{
    enum { encoded_byte_size = 8 };

    bool has_x;
    uint32_t x;

    BuiltinOptional(): has_x(), x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct FixcompOptional
{
    enum { encoded_byte_size = 12 };

    bool has_x;
    Builtin x;

    FixcompOptional(): has_x(), x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Unions_HPP */
