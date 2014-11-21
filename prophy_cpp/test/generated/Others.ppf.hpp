#ifndef _PROPHY_GENERATED_FULL_Others_HPP
#define _PROPHY_GENERATED_FULL_Others_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/array.hpp>
#include <prophy/endianness.hpp>
#include <prophy/optional.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>
#include <prophy/detail/mpl.hpp>

namespace prophy
{
namespace generated
{

enum { CONSTANT = 3 };

typedef uint16_t TU16;

enum Enum
{
    Enum_One = 1,
    Enum_Two = 2
};

struct ConstantTypedefEnum : public prophy::detail::message<ConstantTypedefEnum>
{
    enum { encoded_byte_size = 12 };

    array<uint16_t, CONSTANT> a;
    TU16 b;
    Enum c;

    ConstantTypedefEnum(): a(), b(), c(Enum_One) { }
    ConstantTypedefEnum(const array<uint16_t, CONSTANT>& _1, TU16 _2, Enum _3): a(_1), b(_2), c(_3) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct DynEnum : public prophy::detail::message<DynEnum>
{
    enum { encoded_byte_size = -1 };

    std::vector<Enum> x;

    DynEnum() { }
    DynEnum(const std::vector<Enum>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 4 + x.size() * 4;
    }
};

struct Floats : public prophy::detail::message<Floats>
{
    enum { encoded_byte_size = 16 };

    float a;
    double b;

    Floats(): a(), b() { }
    Floats(float _1, double _2): a(_1), b(_2) { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct BytesFixed : public prophy::detail::message<BytesFixed>
{
    enum { encoded_byte_size = 3 };

    array<uint8_t, 3> x;

    BytesFixed(): x() { }
    BytesFixed(const array<uint8_t, 3>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 3;
    }
};

struct BytesDynamic : public prophy::detail::message<BytesDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    BytesDynamic() { }
    BytesDynamic(const std::vector<uint8_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size() * 1
        );
    }
};

struct BytesLimited : public prophy::detail::message<BytesLimited>
{
    enum { encoded_byte_size = 8 };

    std::vector<uint8_t> x; // limit 4

    BytesLimited() { }
    BytesLimited(const std::vector<uint8_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct BytesGreedy : public prophy::detail::message<BytesGreedy>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x; // greedy

    BytesGreedy() { }
    BytesGreedy(const std::vector<uint8_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return x.size() * 1;
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_Others_HPP */
