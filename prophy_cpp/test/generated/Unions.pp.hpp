#ifndef _PROPHY_GENERATED_Unions_HPP
#define _PROPHY_GENERATED_Unions_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/endianness.hpp>

#include "Arrays.pp.hpp"

struct Union
{
    enum { encoded_byte_size = 12 };

    enum discriminator_t
    {
        discriminator_a = 1,
        discriminator_b = 2,
        discriminator_c = 3
    } discriminator;

    union
    {
        uint8_t a;
        uint32_t b;
        Builtin c;
    };

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinOptional
{
    enum { encoded_byte_size = 8 };

    bool has_x;
    uint32_t x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct FixcompOptional
{
    enum { encoded_byte_size = 8 };

    bool has_x;
    Builtin x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Unions_HPP */
