#ifndef _PROPHY_GENERATED_ManyArraysMixed_HPP
#define _PROPHY_GENERATED_ManyArraysMixed_HPP

#include <prophy/prophy.hpp>

struct ManyArraysMixed
{
    uint32_t num_of_x;
    uint16_t num_of_y;
    uint8_t x[1];

    struct part2
    {
        uint16_t y[1];
    } _2;
};

namespace prophy
{

inline ManyArraysMixed::part2* swap(ManyArraysMixed::part2* payload, size_t num_of_y)
{
    return cast<ManyArraysMixed::part2*>(swap_n_fixed(payload->y, num_of_y));
}

template <>
inline ManyArraysMixed* swap<ManyArraysMixed>(ManyArraysMixed* payload)
{
    swap(&payload->num_of_x);
    swap(&payload->num_of_y);
    ManyArraysMixed::part2* part2 = cast<ManyArraysMixed::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<ManyArraysMixed*>(swap(part2, payload->num_of_y));
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ManyArrays_HPP */
