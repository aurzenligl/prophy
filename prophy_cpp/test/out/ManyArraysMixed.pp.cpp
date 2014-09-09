#include "ManyArraysMixed.pp.hpp"

namespace prophy
{
namespace raw
{

inline ManyArraysMixed::part2* swap(ManyArraysMixed::part2* payload, size_t num_of_y)
{
    return cast<ManyArraysMixed::part2*>(swap_n_fixed(payload->y, num_of_y));
}

template <>
ManyArraysMixed* swap<ManyArraysMixed>(ManyArraysMixed* payload)
{
    swap(&payload->num_of_x);
    swap(&payload->num_of_y);
    ManyArraysMixed::part2* part2 = cast<ManyArraysMixed::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<ManyArraysMixed*>(swap(part2, payload->num_of_y));
}

} // namespace raw
} // namespace prophy
