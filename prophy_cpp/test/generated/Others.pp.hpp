#ifndef _PROPHY_GENERATED_Others_HPP
#define _PROPHY_GENERATED_Others_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>

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

    size_t get_byte_size() const
    {
        return 12;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct Floats
{
    enum { encoded_byte_size = 16 };

    float a;
    double b;

    Floats(): a(), b() { }

    size_t get_byte_size() const
    {
        return 16;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BytesFixed
{
    enum { encoded_byte_size = 3 };

    uint8_t x[3];

    BytesFixed(): x() { }

    size_t get_byte_size() const
    {
        return 3;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BytesDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size()
        );
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BytesLimited
{
    enum { encoded_byte_size = 8 };

    std::vector<uint8_t> x; // limit 4

    size_t get_byte_size() const
    {
        return 8;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BytesGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x; // greedy

    size_t get_byte_size() const
    {
        return x.size();
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

#endif  /* _PROPHY_GENERATED_Others_HPP */
