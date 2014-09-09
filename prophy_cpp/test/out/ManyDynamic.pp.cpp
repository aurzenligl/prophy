#include "ManyDynamic.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
ManyDynamicHelper* swap<ManyDynamicHelper>(ManyDynamicHelper* payload)
{
    swap(&payload->num_of_x);
    return cast<ManyDynamicHelper*>(swap_n_fixed(payload->x, payload->num_of_x));
}

inline ManyDynamic::part2* swap(ManyDynamic::part2* payload)
{
    return cast<ManyDynamic::part2*>(swap(&payload->y));
}

inline ManyDynamic::part3* swap(ManyDynamic::part3* payload)
{
    return cast<ManyDynamic::part3*>(swap(&payload->z));
}

template <>
ManyDynamic* swap<ManyDynamic>(ManyDynamic* payload)
{
    ManyDynamic::part2* part2 = cast<ManyDynamic::part2*>(swap(&payload->x));
    ManyDynamic::part3* part3 = cast<ManyDynamic::part3*>(swap(part2));
    return cast<ManyDynamic*>(swap(part3));
}

} // namespace raw
} // namespace prophy
