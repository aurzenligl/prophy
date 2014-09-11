#include "Arrays.ppr.hpp"

using namespace raw;

namespace prophy
{

template <>
Builtin* swap<Builtin>(Builtin* payload)
{
    swap(&payload->a);
    swap(&payload->b);
    return payload + 1;
}

template <>
BuiltinFixed* swap<BuiltinFixed>(BuiltinFixed* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

template <>
BuiltinDynamic* swap<BuiltinDynamic>(BuiltinDynamic* payload)
{
    swap(&payload->num_of_x);
    return cast<BuiltinDynamic*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
BuiltinLimited* swap<BuiltinLimited>(BuiltinLimited* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}

template <>
BuiltinGreedy* swap<BuiltinGreedy>(BuiltinGreedy* payload)
{
    swap(&payload->x);
    return cast<BuiltinGreedy*>(payload->y);
}

template <>
Fixcomp* swap<Fixcomp>(Fixcomp* payload)
{
    swap(&payload->a);
    swap(&payload->b);
    return payload + 1;
}

template <>
FixcompFixed* swap<FixcompFixed>(FixcompFixed* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

template <>
FixcompDynamic* swap<FixcompDynamic>(FixcompDynamic* payload)
{
    swap(&payload->num_of_x);
    return cast<FixcompDynamic*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
FixcompLimited* swap<FixcompLimited>(FixcompLimited* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}

template <>
FixcompGreedy* swap<FixcompGreedy>(FixcompGreedy* payload)
{
    swap(&payload->x);
    return cast<FixcompGreedy*>(payload->y);
}

template <>
Dyncomp* swap<Dyncomp>(Dyncomp* payload)
{
    return cast<Dyncomp*>(swap(&payload->x));
}

template <>
DyncompDynamic* swap<DyncompDynamic>(DyncompDynamic* payload)
{
    swap(&payload->num_of_x);
    return cast<DyncompDynamic*>(swap_n_dynamic(payload->x, payload->num_of_x));
}

template <>
DyncompGreedy* swap<DyncompGreedy>(DyncompGreedy* payload)
{
    swap(&payload->x);
    return cast<DyncompGreedy*>(payload->y);
}

} // namespace prophy
