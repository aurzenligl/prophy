#ifndef _PROPHY_GENERATED_Others_HPP
#define _PROPHY_GENERATED_Others_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>

enum { CONSTANT = 3 };

typedef uint16_t TU16;

enum Enum
{
    Enum_One = 1,
    Enum_Two = 2
};

struct ConstantTypedefEnum : prophy::detail::message<ConstantTypedefEnum>
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
};

struct DynEnum : prophy::detail::message<DynEnum>
{
    enum { encoded_byte_size = -1 };

    std::vector<Enum> x;

    DynEnum() { }

    size_t get_byte_size() const
    {
        return 4 + x.size() * 4;
    }
};

struct Floats : prophy::detail::message<Floats>
{
    enum { encoded_byte_size = 16 };

    float a;
    double b;

    Floats(): a(), b() { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct BytesFixed : prophy::detail::message<BytesFixed>
{
    enum { encoded_byte_size = 3 };

    uint8_t x[3];

    BytesFixed(): x() { }

    size_t get_byte_size() const
    {
        return 3;
    }
};

struct BytesDynamic : prophy::detail::message<BytesDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size() * 1
        );
    }
};

struct BytesLimited : prophy::detail::message<BytesLimited>
{
    enum { encoded_byte_size = 8 };

    std::vector<uint8_t> x; // limit 4

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct BytesGreedy : prophy::detail::message<BytesGreedy>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x; // greedy

    size_t get_byte_size() const
    {
        return x.size() * 1;
    }
};

#endif  /* _PROPHY_GENERATED_Others_HPP */
