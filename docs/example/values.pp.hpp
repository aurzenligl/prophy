#ifndef _PROPHY_GENERATED_values_HPP
#define _PROPHY_GENERATED_values_HPP

#include <prophy/prophy.hpp>

PROPHY_STRUCT(4) Keys
{
    uint32_t key_a;
    uint32_t key_b;
    uint32_t key_c;
};

PROPHY_STRUCT(4) Nodes
{
    uint32_t num_of_nodes;
    uint32_t nodes[3]; /// limited array, size in num_of_nodes
};

PROPHY_STRUCT(4) Token
{
    enum _discriminator
    {
        discriminator_id = 0,
        discriminator_keys = 1,
        discriminator_nodes = 2
    } discriminator;

    union
    {
        uint32_t id;
        Keys keys;
        Nodes nodes;
    };
};

PROPHY_STRUCT(8) Object
{
    Token token;
    uint32_t num_of_values;
    int64_t values[1]; /// dynamic array, size in num_of_values

    PROPHY_STRUCT(4) part2
    {
        uint32_t num_of_updated_values;
        uint8_t updated_values[1]; /// dynamic array, size in num_of_updated_values
    } _2;
};

PROPHY_STRUCT(8) Values
{
    uint32_t transaction_id;
    uint32_t num_of_objects;
    Object objects[1]; /// dynamic array, size in num_of_objects
};

namespace prophy
{

template <> Keys* swap<Keys>(Keys*);
template <> Nodes* swap<Nodes>(Nodes*);
template <> Token* swap<Token>(Token*);
template <> Object* swap<Object>(Object*);
template <> Values* swap<Values>(Values*);

} // namespace prophy

#endif  /* _PROPHY_GENERATED_values_HPP */
