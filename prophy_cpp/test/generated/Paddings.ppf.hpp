#ifndef _PROPHY_GENERATED_FULL_Paddings_HPP
#define _PROPHY_GENERATED_FULL_Paddings_HPP

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

struct Endpad : public prophy::detail::message<Endpad>
{
    enum { encoded_byte_size = 4 };

    uint16_t x;
    uint8_t y;

    Endpad(): x(), y() { }
    Endpad(uint16_t _1, uint8_t _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct EndpadFixed : public prophy::detail::message<EndpadFixed>
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    array<uint8_t, 3> y;

    EndpadFixed(): x(), y() { }
    EndpadFixed(uint32_t _1, const array<uint8_t, 3>& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct EndpadDynamic : public prophy::detail::message<EndpadDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    EndpadDynamic() { }
    EndpadDynamic(const std::vector<uint8_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size() * 1
        );
    }
};

struct EndpadLimited : public prophy::detail::message<EndpadLimited>
{
    enum { encoded_byte_size = 8 };

    std::vector<uint8_t> x; /// limit 2

    EndpadLimited() { }
    EndpadLimited(const std::vector<uint8_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct EndpadGreedy : public prophy::detail::message<EndpadGreedy>
{
    enum { encoded_byte_size = -1 };

    uint32_t x;
    std::vector<uint8_t> y; /// greedy

    EndpadGreedy(): x() { }
    EndpadGreedy(uint32_t _1, const std::vector<uint8_t>& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + y.size() * 1
        );
    }
};

struct Scalarpad : public prophy::detail::message<Scalarpad>
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    uint16_t y;

    Scalarpad(): x(), y() { }
    Scalarpad(uint8_t _1, uint16_t _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct ScalarpadComppre_Helper : public prophy::detail::message<ScalarpadComppre_Helper>
{
    enum { encoded_byte_size = 1 };

    uint8_t x;

    ScalarpadComppre_Helper(): x() { }
    ScalarpadComppre_Helper(uint8_t _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 1;
    }
};

struct ScalarpadComppre : public prophy::detail::message<ScalarpadComppre>
{
    enum { encoded_byte_size = 4 };

    ScalarpadComppre_Helper x;
    uint16_t y;

    ScalarpadComppre(): y() { }
    ScalarpadComppre(const ScalarpadComppre_Helper& _1, uint16_t _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct ScalarpadComppost_Helper : public prophy::detail::message<ScalarpadComppost_Helper>
{
    enum { encoded_byte_size = 2 };

    uint16_t x;

    ScalarpadComppost_Helper(): x() { }
    ScalarpadComppost_Helper(uint16_t _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 2;
    }
};

struct ScalarpadComppost : public prophy::detail::message<ScalarpadComppost>
{
    enum { encoded_byte_size = 4 };

    uint8_t x;
    ScalarpadComppost_Helper y;

    ScalarpadComppost(): x() { }
    ScalarpadComppost(uint8_t _1, const ScalarpadComppost_Helper& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 4;
    }
};

struct UnionpadOptionalboolpad : public prophy::detail::message<UnionpadOptionalboolpad>
{
    enum { encoded_byte_size = 12 };

    uint8_t x;
    optional<uint8_t> y;

    UnionpadOptionalboolpad(): x() { }
    UnionpadOptionalboolpad(uint8_t _1, const optional<uint8_t>& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct UnionpadOptionalvaluepad : public prophy::detail::message<UnionpadOptionalvaluepad>
{
    enum { encoded_byte_size = 16 };

    optional<uint64_t> x;

    UnionpadOptionalvaluepad() { }
    UnionpadOptionalvaluepad(const optional<uint64_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct UnionpadDiscpad_Helper : public prophy::detail::message<UnionpadDiscpad_Helper>
{
    enum { encoded_byte_size = 8 };

    enum _discriminator
    {
        discriminator_a = 1
    } discriminator;

    static const prophy::detail::int2type<discriminator_a> discriminator_a_t;

    uint8_t a;

    UnionpadDiscpad_Helper(): discriminator(discriminator_a), a() { }
    UnionpadDiscpad_Helper(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct UnionpadDiscpad : public prophy::detail::message<UnionpadDiscpad>
{
    enum { encoded_byte_size = 12 };

    uint8_t x;
    UnionpadDiscpad_Helper y;

    UnionpadDiscpad(): x() { }
    UnionpadDiscpad(uint8_t _1, const UnionpadDiscpad_Helper& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct UnionpadArmpad_Helper : public prophy::detail::message<UnionpadArmpad_Helper>
{
    enum { encoded_byte_size = 16 };

    enum _discriminator
    {
        discriminator_a = 1,
        discriminator_b = 2
    } discriminator;

    static const prophy::detail::int2type<discriminator_a> discriminator_a_t;
    static const prophy::detail::int2type<discriminator_b> discriminator_b_t;

    uint8_t a;
    uint64_t b;

    UnionpadArmpad_Helper(): discriminator(discriminator_a), a(), b() { }
    UnionpadArmpad_Helper(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }
    UnionpadArmpad_Helper(prophy::detail::int2type<discriminator_b>, uint64_t _1): discriminator(discriminator_b), b(_1) { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct UnionpadArmpad : public prophy::detail::message<UnionpadArmpad>
{
    enum { encoded_byte_size = 24 };

    uint8_t x;
    UnionpadArmpad_Helper y;

    UnionpadArmpad(): x() { }
    UnionpadArmpad(uint8_t _1, const UnionpadArmpad_Helper& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 24;
    }
};

struct ArraypadCounter : public prophy::detail::message<ArraypadCounter>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint16_t> x;

    ArraypadCounter() { }
    ArraypadCounter(const std::vector<uint16_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 2 + 2 * x.size();
    }
};

struct ArraypadCounterSeparated : public prophy::detail::message<ArraypadCounterSeparated>
{
    enum { encoded_byte_size = -1 };

    uint32_t y;
    std::vector<uint32_t> x;

    ArraypadCounterSeparated(): y() { }
    ArraypadCounterSeparated(uint32_t _1, const std::vector<uint32_t>& _2): y(_1), x(_2) { }

    size_t get_byte_size() const
    {
        return 8 + 4 * x.size();
    }
};

struct ArraypadCounterAligns_Helper : public prophy::detail::message<ArraypadCounterAligns_Helper>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    ArraypadCounterAligns_Helper() { }
    ArraypadCounterAligns_Helper(const std::vector<uint8_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<2>(
            2 + x.size()
        );
    }
};

struct ArraypadCounterAligns : public prophy::detail::message<ArraypadCounterAligns>
{
    enum { encoded_byte_size = -1 };

    uint8_t x;
    ArraypadCounterAligns_Helper y;

    ArraypadCounterAligns(): x() { }
    ArraypadCounterAligns(uint8_t _1, const ArraypadCounterAligns_Helper& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 2 + y.get_byte_size();
    }
};

struct ArraypadFixed : public prophy::detail::message<ArraypadFixed>
{
    enum { encoded_byte_size = 12 };

    uint32_t x;
    array<uint8_t, 3> y;
    uint32_t z;

    ArraypadFixed(): x(), y(), z() { }
    ArraypadFixed(uint32_t _1, const array<uint8_t, 3>& _2, uint32_t _3): x(_1), y(_2), z(_3) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct ArraypadDynamic : public prophy::detail::message<ArraypadDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    uint32_t y;

    ArraypadDynamic(): y() { }
    ArraypadDynamic(const std::vector<uint8_t>& _1, uint32_t _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size()
        ) + 4;
    }
};

struct ArraypadLimited : public prophy::detail::message<ArraypadLimited>
{
    enum { encoded_byte_size = 12 };

    std::vector<uint8_t> x; // limit 2
    uint32_t y;

    ArraypadLimited(): y() { }
    ArraypadLimited(const std::vector<uint8_t>& _1, uint32_t _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_Paddings_HPP */
