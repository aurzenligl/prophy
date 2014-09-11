#include "Arrays.ppr.hpp"

namespace prophy
{

template <>
raw::Builtin* swap<raw::Builtin>(raw::Builtin* payload)
{
    swap(&payload->a);
    swap(&payload->b);
    return payload + 1;
}

template <>
raw::BuiltinFixed* swap<raw::BuiltinFixed>(raw::BuiltinFixed* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

template <>
raw::BuiltinDynamic* swap<raw::BuiltinDynamic>(raw::BuiltinDynamic* payload)
{
    swap(&payload->num_of_x);
    return cast<raw::BuiltinDynamic*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
raw::BuiltinLimited* swap<raw::BuiltinLimited>(raw::BuiltinLimited* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}

template <>
raw::BuiltinGreedy* swap<raw::BuiltinGreedy>(raw::BuiltinGreedy* payload)
{
    swap(&payload->x);
    return cast<raw::BuiltinGreedy*>(payload->y);
}

} // namespace prophy
