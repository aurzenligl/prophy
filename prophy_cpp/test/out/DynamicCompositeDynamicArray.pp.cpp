#include "DynamicCompositeDynamicArray.pp.hpp"

namespace prophy
{

template <>
DynamicCompositeDynamicArray* swap<DynamicCompositeDynamicArray>(DynamicCompositeDynamicArray* payload)
{
    swap(&payload->num_of_x);
    return cast<DynamicCompositeDynamicArray*>(swap_n_dynamic(payload->x, payload->num_of_x));
}

} // namespace prophy
