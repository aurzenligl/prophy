#include "ManyArraysMixedHeavily.pp.hpp"

namespace prophy
{
namespace raw
{

inline ManyArraysMixedHeavily::part2* swap(ManyArraysMixedHeavily::part2* payload)
{
    swap(&payload->num_of_c);
    return cast<ManyArraysMixedHeavily::part2*>(swap_n_fixed(payload->c, payload->num_of_c));
}

inline ManyArraysMixedHeavily::part3* swap(ManyArraysMixedHeavily::part3* payload, size_t num_of_a)
{
    return cast<ManyArraysMixedHeavily::part3*>(swap_n_fixed(payload->a, num_of_a));
}

template <>
ManyArraysMixedHeavily* swap<ManyArraysMixedHeavily>(ManyArraysMixedHeavily* payload)
{
    swap(&payload->num_of_a);
    swap(&payload->num_of_b);
    ManyArraysMixedHeavily::part2* part2 = cast<ManyArraysMixedHeavily::part2*>(swap_n_fixed(payload->b, payload->num_of_b));
    ManyArraysMixedHeavily::part3* part3 = cast<ManyArraysMixedHeavily::part3*>(swap(part2));
    return cast<ManyArraysMixedHeavily*>(swap(part3, payload->num_of_a));
}

} // namespace raw
} // namespace prophy
