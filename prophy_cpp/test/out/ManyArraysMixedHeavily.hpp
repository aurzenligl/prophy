#ifndef _PROPHY_GENERATED_ManyArraysMixedHeavily_HPP
#define _PROPHY_GENERATED_ManyArraysMixedHeavily_HPP

#include <prophy/prophy.hpp>

struct ManyArraysMixedHeavily
{
    uint32_t num_of_a;
    uint32_t num_of_b;
    uint16_t b[1];

    struct part2
    {
        uint32_t num_of_c;
        uint16_t c[1];
    } _2;

    struct part3
    {
        uint16_t a[1];
    } _3;
};

namespace prophy
{

inline ManyArraysMixedHeavily::part3* swap(ManyArraysMixedHeavily::part3* payload, size_t num_of_a)
{
    return cast<ManyArraysMixedHeavily::part3*>(swap_n_fixed(payload->a, num_of_a));
}

inline ManyArraysMixedHeavily::part2* swap(ManyArraysMixedHeavily::part2* payload)
{
    swap(&payload->num_of_c);
    return cast<ManyArraysMixedHeavily::part2*>(swap_n_fixed(payload->c, payload->num_of_c));
}

template <>
inline ManyArraysMixedHeavily* swap<ManyArraysMixedHeavily>(ManyArraysMixedHeavily* payload)
{
    swap(&payload->num_of_a);
    swap(&payload->num_of_b);
    ManyArraysMixedHeavily::part2* part2 = cast<ManyArraysMixedHeavily::part2*>(swap_n_fixed(payload->b, payload->num_of_b));
    ManyArraysMixedHeavily::part3* part3 = cast<ManyArraysMixedHeavily::part3*>(swap(part2));
    return cast<ManyArraysMixedHeavily*>(swap(part3, payload->num_of_a));
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ManyArraysMixedHeavily_HPP */
