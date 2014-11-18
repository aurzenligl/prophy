#ifndef _PROPHY_GENERATED_FULL_values_HPP
#define _PROPHY_GENERATED_FULL_values_HPP

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

struct Keys : public prophy::detail::message<Keys>
{
    enum { encoded_byte_size = 12 };

    uint32_t key_a;
    uint32_t key_b;
    uint32_t key_c;

    Keys(): key_a(), key_b(), key_c() { }
    Keys(uint32_t _1, uint32_t _2, uint32_t _3): key_a(_1), key_b(_2), key_c(_3) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct Nodes : public prophy::detail::message<Nodes>
{
    enum { encoded_byte_size = 16 };

    std::vector<uint32_t> nodes; /// limit 3

    Nodes() { }
    Nodes(const std::vector<uint32_t>& _1): nodes(_1) { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct Token : public prophy::detail::message<Token>
{
    enum { encoded_byte_size = 20 };

    enum _discriminator
    {
        discriminator_id = 0,
        discriminator_keys = 1,
        discriminator_nodes = 2
    } discriminator;

    static const prophy::detail::int2type<discriminator_id> discriminator_id_t;
    static const prophy::detail::int2type<discriminator_keys> discriminator_keys_t;
    static const prophy::detail::int2type<discriminator_nodes> discriminator_nodes_t;

    uint32_t id;
    Keys keys;
    Nodes nodes;

    Token(): discriminator(discriminator_id), id() { }
    Token(prophy::detail::int2type<discriminator_id>, uint32_t _1): discriminator(discriminator_id), id(_1) { }
    Token(prophy::detail::int2type<discriminator_keys>, const Keys& _1): discriminator(discriminator_keys), keys(_1) { }
    Token(prophy::detail::int2type<discriminator_nodes>, const Nodes& _1): discriminator(discriminator_nodes), nodes(_1) { }

    size_t get_byte_size() const
    {
        return 20;
    }
};

struct Object : public prophy::detail::message<Object>
{
    enum { encoded_byte_size = -1 };

    Token token;
    std::vector<int64_t> values;
    std::vector<uint8_t> updated_values;

    Object() { }
    Object(const Token& _1, const std::vector<int64_t>& _2, const std::vector<uint8_t>& _3): token(_1), values(_2), updated_values(_3) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<8>(
            values.size() * 8 + updated_values.size() * 1 + 28
        );
    }
};

struct Values : public prophy::detail::message<Values>
{
    enum { encoded_byte_size = -1 };

    uint32_t transaction_id;
    std::vector<Object> objects;

    Values(): transaction_id() { }
    Values(uint32_t _1, const std::vector<Object>& _2): transaction_id(_1), objects(_2) { }

    size_t get_byte_size() const
    {
        return std::accumulate(objects.begin(), objects.end(), size_t(), prophy::detail::byte_size()) + 8;
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_values_HPP */
