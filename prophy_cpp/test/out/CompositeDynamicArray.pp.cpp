#include "CompositeDynamicArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
CompositeDynamicArray* swap<CompositeDynamicArray>(CompositeDynamicArray* payload)
{
    swap(&payload->num_of_x);
    return cast<CompositeDynamicArray*>(swap_n_fixed(payload->x, payload->num_of_x));
}

} // namespace raw
} // namespace prophy
