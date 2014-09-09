#include "CompositeFixedArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
CompositeFixedArray* swap<CompositeFixedArray>(CompositeFixedArray* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

} // namespace raw
} // namespace prophy
