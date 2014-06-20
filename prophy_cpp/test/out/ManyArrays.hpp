#ifndef _PROPHY_GENERATED_ManyArrays_HPP
#define _PROPHY_GENERATED_ManyArrays_HPP

#include <prophy/prophy.hpp>

struct ManyArrays
{
    uint32_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint16_t num_of_y;
        uint16_t y[1];
    } _2;

    struct part3
    {
        uint8_t num_of_z;
        uint64_t z[1];
    } _3;
};

namespace prophy
{

template <>
inline ManyArrays::part2* swap<ManyArrays::part2>(ManyArrays::part2& payload)
{
    swap(payload.num_of_y);
    return cast<ManyArrays::part2*>(
        swap_n_fixed(payload.y, payload.num_of_y));
}

template <>
inline ManyArrays::part3* swap<ManyArrays::part3>(ManyArrays::part3& payload)
{
    swap(payload.num_of_z);
    return cast<ManyArrays::part3*>(
        swap_n_fixed(payload.z, payload.num_of_z));
}

template <>
inline ManyArrays* swap<ManyArrays>(ManyArrays& payload)
{
    swap(payload.num_of_x);
    return cast<ManyArrays*>(
        swap(*cast<ManyArrays::part3*>(
            swap(*cast<ManyArrays::part2*>(
                swap_n_fixed(payload.x, payload.num_of_x)
            ))
        ))
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ManyArrays_HPP */
