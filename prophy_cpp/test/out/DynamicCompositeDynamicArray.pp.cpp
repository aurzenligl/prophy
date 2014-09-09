#include "DynamicCompositeDynamicArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
DynamicCompositeDynamicArray* swap<DynamicCompositeDynamicArray>(DynamicCompositeDynamicArray* payload)
{
    swap(&payload->num_of_x);
    return cast<DynamicCompositeDynamicArray*>(swap_n_dynamic(payload->x, payload->num_of_x));
}

} // namespace raw
} // namespace prophy
