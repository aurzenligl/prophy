#ifndef _PROPHY_GENERATED_Paddings_HPP
#define _PROPHY_GENERATED_Paddings_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>

struct Endpad
{
    enum { encoded_byte_size = 4 };

    uint16_t x;
    uint8_t y;

    Endpad(): x(), y() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct EndpadFixed
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint8_t y[3];

    EndpadFixed(): x(), y() { }

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

    EndpadGreedy(): x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct Scalarpad
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    uint16_t y;

    Scalarpad(): x(), y() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppre_Helper
{
    enum { encoded_byte_size = 1 };

    uint8_t x;

    ScalarpadComppre_Helper(): x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppre
{
    enum { encoded_byte_size = 4 };

    ScalarpadComppre_Helper x;
    uint16_t y;

    ScalarpadComppre(): y() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppost_Helper
{
    enum { encoded_byte_size = 2 };

    uint16_t x;

    ScalarpadComppost_Helper(): x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ScalarpadComppost
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    ScalarpadComppost_Helper y;

    ScalarpadComppost(): x() { }

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

    UnionpadOptionalboolpad(): x(), has_y(), y() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadOptionalvaluepad
{
    enum { encoded_byte_size = 16 };

    bool has_x;
    uint64_t x;

    UnionpadOptionalvaluepad(): has_x(), x() { }

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

    uint8_t a;

    UnionpadDiscpad_Helper(): discriminator(discriminator_a), a() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadDiscpad
{
    enum { encoded_byte_size = 16 };

    uint8_t x;
    UnionpadDiscpad_Helper y;

    UnionpadDiscpad(): x() { }

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

    uint8_t a;
    uint64_t b;

    UnionpadArmpad_Helper(): discriminator(discriminator_a), a(), b() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct UnionpadArmpad
{
    enum { encoded_byte_size = 24 };

    uint8_t x;
    UnionpadArmpad_Helper y;

    UnionpadArmpad(): x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ArraypadCounter
{
    enum { encoded_byte_size = -1 };

    std::vector<uint16_t> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ArraypadCounterSeparated
{
    enum { encoded_byte_size = -1 };

    uint32_t y;
    std::vector<uint32_t> x;

    ArraypadCounterSeparated(): y() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ArraypadCounterAligns_Helper
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ArraypadCounterAligns
{
    enum { encoded_byte_size = -1 };

    uint8_t x;
    ArraypadCounterAligns_Helper y;

    ArraypadCounterAligns(): x() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ArraypadFixed
{
    enum { encoded_byte_size = 12 };

    uint32_t x;
    uint8_t y[3];
    uint32_t z;

    ArraypadFixed(): x(), y(), z() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ArraypadDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    uint32_t y;

    ArraypadDynamic(): y() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct ArraypadLimited
{
    enum { encoded_byte_size = 12 };

    std::vector<uint8_t> x; // limit 4
    uint32_t y;

    ArraypadLimited(): y() { }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Paddings_HPP */
