#ifndef _PROPHY_GENERATED_ManyDynamic_HPP
#define _PROPHY_GENERATED_ManyDynamic_HPP

#include <prophy/prophy.hpp>

struct ManyDynamicHelper
{
    uint32_t num_of_x;
    uint16_t x[1];
};

struct ManyDynamic
{
    ManyDynamicHelper x;

    struct part2
    {
        ManyDynamicHelper y;
    } _2;

    struct part3
    {
        ManyDynamicHelper z;
    } _3;
};

namespace prophy
{

template <>
inline ManyDynamicHelper* swap<ManyDynamicHelper>(ManyDynamicHelper* payload)
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
inline ManyDynamic* swap<ManyDynamic>(ManyDynamic* payload)
{
    ManyDynamic::part2* part2 = cast<ManyDynamic::part2*>(swap(&payload->x));
    ManyDynamic::part3* part3 = cast<ManyDynamic::part3*>(swap(part2));
    return cast<ManyDynamic*>(swap(part3));
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ManyDynamic_HPP */
