#include "values.ppf.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include <prophy/detail/printer.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy::generated;

namespace prophy
{
namespace detail
{

template <>
template <endianness E>
uint8_t* message_impl<Keys>::encode(const Keys& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.key_a);
    pos = do_encode<E>(pos, x.key_b);
    pos = do_encode<E>(pos, x.key_c);
    return pos;
}
template uint8_t* message_impl<Keys>::encode<native>(const Keys& x, uint8_t* pos);
template uint8_t* message_impl<Keys>::encode<little>(const Keys& x, uint8_t* pos);
template uint8_t* message_impl<Keys>::encode<big>(const Keys& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Keys>::decode(Keys& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.key_a, pos, end) &&
        do_decode<E>(x.key_b, pos, end) &&
        do_decode<E>(x.key_c, pos, end)
    );
}
template bool message_impl<Keys>::decode<native>(Keys& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Keys>::decode<little>(Keys& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Keys>::decode<big>(Keys& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Keys>::print(const Keys& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "key_a", x.key_a);
    do_print(out, indent, "key_b", x.key_b);
    do_print(out, indent, "key_c", x.key_c);
}
template void message_impl<Keys>::print(const Keys& x, std::ostream& out, size_t indent);

template <>
template <endianness E>
uint8_t* message_impl<Nodes>::encode(const Nodes& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(std::min(x.nodes.size(), size_t(3))));
    do_encode<E>(pos, x.nodes.data(), uint32_t(std::min(x.nodes.size(), size_t(3))));
    pos = pos + 12;
    return pos;
}
template uint8_t* message_impl<Nodes>::encode<native>(const Nodes& x, uint8_t* pos);
template uint8_t* message_impl<Nodes>::encode<little>(const Nodes& x, uint8_t* pos);
template uint8_t* message_impl<Nodes>::encode<big>(const Nodes& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Nodes>::decode(Nodes& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.nodes, pos, end, 3) &&
        do_decode_in_place<E>(x.nodes.data(), x.nodes.size(), pos, end) &&
        do_decode_advance(12, pos, end)
    );
}
template bool message_impl<Nodes>::decode<native>(Nodes& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Nodes>::decode<little>(Nodes& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Nodes>::decode<big>(Nodes& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Nodes>::print(const Nodes& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "nodes", x.nodes.data(), std::min(x.nodes.size(), size_t(3)));
}
template void message_impl<Nodes>::print(const Nodes& x, std::ostream& out, size_t indent);

template <>
template <endianness E>
uint8_t* message_impl<Token>::encode(const Token& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.discriminator);
    switch (x.discriminator)
    {
        case Token::discriminator_id: do_encode<E>(pos, x.id); break;
        case Token::discriminator_keys: do_encode<E>(pos, x.keys); break;
        case Token::discriminator_nodes: do_encode<E>(pos, x.nodes); break;
    }
    pos = pos + 16;
    return pos;
}
template uint8_t* message_impl<Token>::encode<native>(const Token& x, uint8_t* pos);
template uint8_t* message_impl<Token>::encode<little>(const Token& x, uint8_t* pos);
template uint8_t* message_impl<Token>::encode<big>(const Token& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Token>::decode(Token& x, const uint8_t*& pos, const uint8_t* end)
{
    if (!do_decode<E>(x.discriminator, pos, end)) return false;
    switch (x.discriminator)
    {
        case Token::discriminator_id: if (!do_decode_in_place<E>(x.id, pos, end)) return false; break;
        case Token::discriminator_keys: if (!do_decode_in_place<E>(x.keys, pos, end)) return false; break;
        case Token::discriminator_nodes: if (!do_decode_in_place<E>(x.nodes, pos, end)) return false; break;
        default: return false;
    }
    return do_decode_advance(16, pos, end);
}
template bool message_impl<Token>::decode<native>(Token& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Token>::decode<little>(Token& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Token>::decode<big>(Token& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Token>::print(const Token& x, std::ostream& out, size_t indent)
{
    switch (x.discriminator)
    {
        case Token::discriminator_id: do_print(out, indent, "id", x.id); break;
        case Token::discriminator_keys: do_print(out, indent, "keys", x.keys); break;
        case Token::discriminator_nodes: do_print(out, indent, "nodes", x.nodes); break;
    }
}
template void message_impl<Token>::print(const Token& x, std::ostream& out, size_t indent);

template <>
template <endianness E>
uint8_t* message_impl<Object>::encode(const Object& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.token);
    pos = do_encode<E>(pos, uint32_t(x.values.size()));
    pos = do_encode<E>(pos, x.values.data(), uint32_t(x.values.size()));
    pos = do_encode<E>(pos, uint32_t(x.updated_values.size()));
    pos = do_encode<E>(pos, x.updated_values.data(), uint32_t(x.updated_values.size()));
    pos = align<8>(pos);
    return pos;
}
template uint8_t* message_impl<Object>::encode<native>(const Object& x, uint8_t* pos);
template uint8_t* message_impl<Object>::encode<little>(const Object& x, uint8_t* pos);
template uint8_t* message_impl<Object>::encode<big>(const Object& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Object>::decode(Object& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.token, pos, end) &&
        do_decode_resize<E, uint32_t>(x.values, pos, end) &&
        do_decode<E>(x.values.data(), x.values.size(), pos, end) &&
        do_decode_resize<E, uint32_t>(x.updated_values, pos, end) &&
        do_decode<E>(x.updated_values.data(), x.updated_values.size(), pos, end) &&
        do_decode_align<8>(pos, end)
    );
}
template bool message_impl<Object>::decode<native>(Object& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Object>::decode<little>(Object& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Object>::decode<big>(Object& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Object>::print(const Object& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "token", x.token);
    do_print(out, indent, "values", x.values.data(), x.values.size());
    do_print(out, indent, "updated_values", std::make_pair(x.updated_values.data(), x.updated_values.size()));
}
template void message_impl<Object>::print(const Object& x, std::ostream& out, size_t indent);

template <>
template <endianness E>
uint8_t* message_impl<Values>::encode(const Values& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.transaction_id);
    pos = do_encode<E>(pos, uint32_t(x.objects.size()));
    pos = do_encode<E>(pos, x.objects.data(), uint32_t(x.objects.size()));
    return pos;
}
template uint8_t* message_impl<Values>::encode<native>(const Values& x, uint8_t* pos);
template uint8_t* message_impl<Values>::encode<little>(const Values& x, uint8_t* pos);
template uint8_t* message_impl<Values>::encode<big>(const Values& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<Values>::decode(Values& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.transaction_id, pos, end) &&
        do_decode_resize<E, uint32_t>(x.objects, pos, end) &&
        do_decode<E>(x.objects.data(), x.objects.size(), pos, end)
    );
}
template bool message_impl<Values>::decode<native>(Values& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Values>::decode<little>(Values& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Values>::decode<big>(Values& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<Values>::print(const Values& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "transaction_id", x.transaction_id);
    do_print(out, indent, "objects", x.objects.data(), x.objects.size());
}
template void message_impl<Values>::print(const Values& x, std::ostream& out, size_t indent);

} // namespace detail
} // namespace prophy
