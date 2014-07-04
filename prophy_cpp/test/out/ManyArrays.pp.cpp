#include "ManyArrays.pp.hpp"

namespace prophy
{

inline ManyArrays::part2* swap(ManyArrays::part2* payload)
{
    swap(&payload->num_of_y);
    return cast<ManyArrays::part2*>(swap_n_fixed(payload->y, payload->num_of_y));
}

inline ManyArrays::part3* swap(ManyArrays::part3* payload)
{
    swap(&payload->num_of_z);
    return cast<ManyArrays::part3*>(swap_n_fixed(payload->z, payload->num_of_z));
}

template <>
ManyArrays* swap<ManyArrays>(ManyArrays* payload)
{
    swap(&payload->num_of_x);
    ManyArrays::part2* part2 = cast<ManyArrays::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    ManyArrays::part3* part3 = cast<ManyArrays::part3*>(swap(part2));
    return cast<ManyArrays*>(swap(part3));
}

} // namespace prophy
