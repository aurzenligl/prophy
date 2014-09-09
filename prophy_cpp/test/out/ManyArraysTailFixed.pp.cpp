#include "ManyArraysTailFixed.pp.hpp"

namespace prophy
{
namespace raw
{

inline ManyArraysTailFixed::part2* swap(ManyArraysTailFixed::part2* payload)
{
    swap(&payload->y);
    swap(&payload->z);
    return payload + 1;
}

template <>
ManyArraysTailFixed* swap<ManyArraysTailFixed>(ManyArraysTailFixed* payload)
{
    swap(&payload->num_of_x);
    ManyArraysTailFixed::part2* part2 = cast<ManyArraysTailFixed::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<ManyArraysTailFixed*>(swap(part2));
}

} // namespace raw
} // namespace prophy
