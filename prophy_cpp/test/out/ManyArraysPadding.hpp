#ifndef _PROPHY_GENERATED_ManyArraysPadding_HPP
#define _PROPHY_GENERATED_ManyArraysPadding_HPP

#include <prophy/prophy.hpp>

struct ManyArraysPaddingInner
{
    uint8_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint32_t num_of_y;
        uint8_t y[1];
    } _2;

    struct part3
    {
        uint64_t z;
    } _3;
};

struct ManyArraysPadding
{
    uint8_t x;
    ManyArraysPaddingInner y;
};

namespace prophy
{

inline ManyArraysPaddingInner::part2* swap(ManyArraysPaddingInner::part2& payload)
{
    swap(payload.num_of_y);
    return cast<ManyArraysPaddingInner::part2*>(
        swap_n_fixed(payload.y, payload.num_of_y));
}

inline ManyArraysPaddingInner::part3* swap(ManyArraysPaddingInner::part3& payload)
{
    swap(payload.z);
    return &payload + 1;
}

template <>
inline ManyArraysPaddingInner* swap<ManyArraysPaddingInner>(ManyArraysPaddingInner& payload)
{
    swap(payload.num_of_x);
    return cast<ManyArraysPaddingInner*>(
        swap(*cast<ManyArraysPaddingInner::part3*>(
            swap(*cast<ManyArraysPaddingInner::part2*>(
                swap_n_fixed(payload.x, payload.num_of_x)
            ))
        ))
    );
}

template <>
inline ManyArraysPadding* swap<ManyArraysPadding>(ManyArraysPadding& payload)
{
    swap(payload.x);
    return cast<ManyArraysPadding*>(
        swap(payload.y)
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ManyArrays_HPP */
