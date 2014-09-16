#ifndef _PROPHY_GENERATED_Others_HPP
#define _PROPHY_GENERATED_Others_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/endianness.hpp>

enum { CONSTANT = 3 };

typedef uint16_t TU16;

enum Enum
{
    Enum_One = 1
};

struct ConstantTypedefEnum
{
    enum { encoded_byte_size = 12 };

    uint16_t a[CONSTANT];
    TU16 b;
    Enum c;

    ConstantTypedefEnum(): a(), b(), c(Enum_One) { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BytesFixed
{
    enum { encoded_byte_size = 3 };

    uint8_t x[3];

    BytesFixed(): x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BytesDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BytesLimited
{
    enum { encoded_byte_size = 8 };

    std::vector<uint8_t> x; // limit 4

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BytesGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x; // greedy

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Others_HPP */
