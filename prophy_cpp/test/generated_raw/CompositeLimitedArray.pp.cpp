#include "CompositeLimitedArray.pp.hpp"

namespace prophy
{

template <>
CompositeLimitedArray* swap<CompositeLimitedArray>(CompositeLimitedArray* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}

} // namespace prophy
