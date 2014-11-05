#ifndef _PROPHY_GENERATED_FULL_Unions_HPP
#define _PROPHY_GENERATED_FULL_Unions_HPP

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

    static const prophy::detail::int2type<discriminator_a> discriminator_a_t;
    static const prophy::detail::int2type<discriminator_b> discriminator_b_t;
    static const prophy::detail::int2type<discriminator_c> discriminator_c_t;

    uint8_t a;
    uint32_t b;
    Builtin c;

    Union(): discriminator(discriminator_a), a(), b() { }
    Union(prophy::detail::int2type<discriminator_a>, uint8_t _1): discriminator(discriminator_a), a(_1) { }
    Union(prophy::detail::int2type<discriminator_b>, uint32_t _1): discriminator(discriminator_b), b(_1) { }
    Union(prophy::detail::int2type<discriminator_c>, const Builtin& _1): discriminator(discriminator_c), c(_1) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct BuiltinOptional : prophy::detail::message<BuiltinOptional>
{
    enum { encoded_byte_size = 8 };

    optional<uint32_t> x;

    BuiltinOptional() { }
    BuiltinOptional(const optional<uint32_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct FixcompOptional : prophy::detail::message<FixcompOptional>
{
    enum { encoded_byte_size = 12 };

    optional<Builtin> x;

    FixcompOptional() { }
    FixcompOptional(const optional<Builtin>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_Unions_HPP */
