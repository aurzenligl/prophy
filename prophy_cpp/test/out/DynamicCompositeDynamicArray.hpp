#ifndef _PROPHY_GENERATED_DynamicCompositeDynamicArray_HPP
#define _PROPHY_GENERATED_DynamicCompositeDynamicArray_HPP

#include <prophy/prophy.hpp>

#include "DynamicComposite.hpp"

struct DynamicCompositeDynamicArray
{
    uint16_t num_of_x;
    DynamicComposite x[1];
};

namespace prophy
{

template <>
inline DynamicCompositeDynamicArray* swap<DynamicCompositeDynamicArray>(DynamicCompositeDynamicArray* payload)
{
    swap(&payload->num_of_x);
    return cast<DynamicCompositeDynamicArray*>(
        swap_n_dynamic(payload->x, payload->num_of_x)
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_DynamicCompositeDynamicArray_HPP */
