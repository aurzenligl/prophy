#ifndef _PROPHY_GENERATED_Paddings_HPP
#define _PROPHY_GENERATED_Paddings_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>

struct Endpad : prophy::detail::message<Endpad>
{
    enum { encoded_byte_size = 4 };

    uint16_t x;
    uint8_t y;

    Endpad(): x(), y() { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct EndpadFixed : prophy::detail::message<EndpadFixed>
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint8_t y[3];

    EndpadFixed(): x(), y() { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct EndpadDynamic : prophy::detail::message<EndpadDynamic>
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

struct EndpadLimited : prophy::detail::message<EndpadLimited>
{
    enum { encoded_byte_size = 8 };

    std::vector<uint8_t> x; /// limit 2

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct EndpadGreedy : prophy::detail::message<EndpadGreedy>
{
    enum { encoded_byte_size = -1 };

    uint32_t x;
    std::vector<uint8_t> y; /// greedy

    EndpadGreedy(): x() { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + y.size() * 1
        );
    }
};

struct Scalarpad : prophy::detail::message<Scalarpad>
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    uint16_t y;

    Scalarpad(): x(), y() { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct ScalarpadComppre_Helper : prophy::detail::message<ScalarpadComppre_Helper>
{
    enum { encoded_byte_size = 1 };

    uint8_t x;

    ScalarpadComppre_Helper(): x() { }

    size_t get_byte_size() const
    {
        return 1;
    }
};

struct ScalarpadComppre : prophy::detail::message<ScalarpadComppre>
{
    enum { encoded_byte_size = 4 };

    ScalarpadComppre_Helper x;
    uint16_t y;

    ScalarpadComppre(): y() { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct ScalarpadComppost_Helper : prophy::detail::message<ScalarpadComppost_Helper>
{
    enum { encoded_byte_size = 2 };

    uint16_t x;

    ScalarpadComppost_Helper(): x() { }

    size_t get_byte_size() const
    {
        return 2;
    }
};

struct ScalarpadComppost : prophy::detail::message<ScalarpadComppost>
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    ScalarpadComppost_Helper y;

    ScalarpadComppost(): x() { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct UnionpadOptionalboolpad : prophy::detail::message<UnionpadOptionalboolpad>
{
    enum { encoded_byte_size = 12 };

    uint8_t x;
    bool has_y;
    uint8_t y;

    UnionpadOptionalboolpad(): x(), has_y(), y() { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct UnionpadOptionalvaluepad : prophy::detail::message<UnionpadOptionalvaluepad>
{
    enum { encoded_byte_size = 16 };

    bool has_x;
    uint64_t x;

    UnionpadOptionalvaluepad(): has_x(), x() { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct UnionpadDiscpad_Helper : prophy::detail::message<UnionpadDiscpad_Helper>
{
    enum { encoded_byte_size = 8 };

    enum _discriminator
    {
        discriminator_a = 1
    } discriminator;

    uint8_t a;

    UnionpadDiscpad_Helper(): discriminator(discriminator_a), a() { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct UnionpadDiscpad : prophy::detail::message<UnionpadDiscpad>
{
    enum { encoded_byte_size = 12 };

    uint8_t x;
    UnionpadDiscpad_Helper y;

    UnionpadDiscpad(): x() { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct UnionpadArmpad_Helper : prophy::detail::message<UnionpadArmpad_Helper>
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

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct UnionpadArmpad : prophy::detail::message<UnionpadArmpad>
{
    enum { encoded_byte_size = 24 };

    uint8_t x;
    UnionpadArmpad_Helper y;

    UnionpadArmpad(): x() { }

    size_t get_byte_size() const
    {
        return 24;
    }
};

struct ArraypadCounter : prophy::detail::message<ArraypadCounter>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint16_t> x;

    size_t get_byte_size() const
    {
        return 2 + 2 * x.size();
    }
};

struct ArraypadCounterSeparated : prophy::detail::message<ArraypadCounterSeparated>
{
    enum { encoded_byte_size = -1 };

    uint32_t y;
    std::vector<uint32_t> x;

    ArraypadCounterSeparated(): y() { }

    size_t get_byte_size() const
    {
        return 8 + 4 * x.size();
    }
};

struct ArraypadCounterAligns_Helper : prophy::detail::message<ArraypadCounterAligns_Helper>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<2>(
            2 + x.size()
        );
    }
};

struct ArraypadCounterAligns : prophy::detail::message<ArraypadCounterAligns>
{
    enum { encoded_byte_size = -1 };

    uint8_t x;
    ArraypadCounterAligns_Helper y;

    ArraypadCounterAligns(): x() { }

    size_t get_byte_size() const
    {
        return 2 + y.get_byte_size();
    }
};

struct ArraypadFixed : prophy::detail::message<ArraypadFixed>
{
    enum { encoded_byte_size = 12 };

    uint32_t x;
    uint8_t y[3];
    uint32_t z;

    ArraypadFixed(): x(), y(), z() { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct ArraypadDynamic : prophy::detail::message<ArraypadDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    uint32_t y;

    ArraypadDynamic(): y() { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size()
        ) + 4;
    }
};

struct ArraypadLimited : prophy::detail::message<ArraypadLimited>
{
    enum { encoded_byte_size = 12 };

    std::vector<uint8_t> x; // limit 2
    uint32_t y;

    ArraypadLimited(): y() { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

#endif  /* _PROPHY_GENERATED_Paddings_HPP */
