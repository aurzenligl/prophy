#include <prophy/detail/prophy.hpp>

#include "values.pp.hpp"

using namespace prophy::detail;

namespace prophy
{

template <>
Keys* swap<Keys>(Keys* payload)
{
    swap(&payload->key_a);
    swap(&payload->key_b);
    swap(&payload->key_c);
    return payload + 1;
}

template <>
Nodes* swap<Nodes>(Nodes* payload)
{
    swap(&payload->num_of_nodes);
    swap_n_fixed(payload->nodes, payload->num_of_nodes);
    return payload + 1;
}

template <>
Token* swap<Token>(Token* payload)
{
    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
    switch (payload->discriminator)
    {
        case Token::discriminator_id: swap(&payload->id); break;
        case Token::discriminator_keys: swap(&payload->keys); break;
        case Token::discriminator_nodes: swap(&payload->nodes); break;
        default: break;
    }
    return payload + 1;
}

inline Object::part2* swap(Object::part2* payload)
{
    swap(&payload->num_of_updated_values);
    return cast<Object::part2*>(swap_n_fixed(payload->updated_values, payload->num_of_updated_values));
}

template <>
Object* swap<Object>(Object* payload)
{
    swap(&payload->token);
    swap(&payload->num_of_values);
    Object::part2* part2 = cast<Object::part2*>(swap_n_fixed(payload->values, payload->num_of_values));
    return cast<Object*>(swap(part2));
}

template <>
Values* swap<Values>(Values* payload)
{
    swap(&payload->transaction_id);
    swap(&payload->num_of_objects);
    return cast<Values*>(swap_n_dynamic(payload->objects, payload->num_of_objects));
}

} // namespace prophy
