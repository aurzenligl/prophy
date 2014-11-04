#ifndef _PROPHY_GENERATED_FULL_Unions_HPP
#define _PROPHY_GENERATED_FULL_Unions_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>
#include <prophy/detail/mpl.hpp>

#include "Arrays.ppf.hpp"

namespace prophy
{
namespace generated
{

struct Union : prophy::detail::message<Union>
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
    Union(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }
    Union(prophy::detail::int2type<discriminator_b>, uint32_t _1): discriminator(discriminator_b), b(_1) { }
    Union(prophy::detail::int2type<discriminator_c>, const Builtin& _1): discriminator(discriminator_c), c(_1) { }
    static Union create_a(uint8_t _1) { return Union(prophy::detail::int2type<discriminator_a>(), _1); }
    static Union create_b(uint32_t _1) { return Union(prophy::detail::int2type<discriminator_b>(), _1); }
    static Union create_c(const Builtin& _1) { return Union(prophy::detail::int2type<discriminator_c>(), _1); }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct BuiltinOptional : prophy::detail::message<BuiltinOptional>
{
    enum { encoded_byte_size = 8 };

    bool has_x;
    uint32_t x;

    BuiltinOptional(): has_x(), x() { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct FixcompOptional : prophy::detail::message<FixcompOptional>
{
    enum { encoded_byte_size = 12 };

    bool has_x;
    Builtin x;

    FixcompOptional(): has_x() { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_Unions_HPP */
