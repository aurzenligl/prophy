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

template <>
inline ManyArraysTailFixed::part2* swap<ManyArraysTailFixed::part2>(ManyArraysTailFixed::part2* payload)
{
    swap(&payload->y);
    swap(&payload->z);
    return payload + 1;
}

template <>
inline ManyArraysTailFixed* swap<ManyArraysTailFixed>(ManyArraysTailFixed* payload)
{
    swap(&payload->num_of_x);
    ManyArraysTailFixed::part2* part2 = cast<ManyArraysTailFixed::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<ManyArraysTailFixed*>(swap(part2));
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ManyArraysTailFixed_HPP */
