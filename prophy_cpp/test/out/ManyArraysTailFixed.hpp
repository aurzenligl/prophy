#ifndef _PROPHY_GENERATED_ManyArraysTailFixed_HPP
#define _PROPHY_GENERATED_ManyArraysTailFixed_HPP

#include <prophy/prophy.hpp>

struct ManyArraysTailFixed
{
    uint8_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint32_t y;
        uint64_t z;
    } _2;
};

namespace prophy
{

inline ManyArraysTailFixed::part2* swap(ManyArraysTailFixed::part2& payload)
{
    swap(payload.y);
    swap(payload.z);
    return &payload + 1;
}

inline ManyArraysTailFixed* swap(ManyArraysTailFixed& payload)
{
    swap(payload.num_of_x);
    return cast<ManyArraysTailFixed*>(
        swap(*cast<ManyArraysTailFixed::part2*>(
            swap_n_fixed(payload.x, payload.num_of_x)
        ))
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ManyArraysTailFixed_HPP */
