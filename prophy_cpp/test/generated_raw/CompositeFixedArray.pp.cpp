#include "CompositeFixedArray.pp.hpp"

namespace prophy
{

template <>
CompositeFixedArray* swap<CompositeFixedArray>(CompositeFixedArray* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

} // namespace prophy
