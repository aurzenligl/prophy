#ifndef _PROPHY_GENERATED_CompositeDynamicArray_HPP
#define _PROPHY_GENERATED_CompositeDynamicArray_HPP

#include <prophy/prophy.hpp>

#include "Scalar.hpp"

struct CompositeDynamicArray
{
    uint32_t num_of_x;
    Scalar x[1];
};

namespace prophy
{

inline CompositeDynamicArray* swap(CompositeDynamicArray& payload)
{
    swap(payload.num_of_x);
    return cast<CompositeDynamicArray*>(
        swap_n_fixed(payload.x, payload.num_of_x)
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_CompositeDynamicArray_HPP */
