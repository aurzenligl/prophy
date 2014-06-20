#ifndef _PROPHY_GENERATED_ScalarDynamicArray_HPP
#define _PROPHY_GENERATED_ScalarDynamicArray_HPP

#include <prophy/prophy.hpp>

struct ScalarDynamicArray
{
    uint32_t num_of_x;
    uint16_t x[1];
};

namespace prophy
{

template <>
inline ScalarDynamicArray* swap<ScalarDynamicArray>(ScalarDynamicArray& payload)
{
    swap(payload.num_of_x);
    return cast<ScalarDynamicArray*>(
        swap_n_fixed(payload.x, payload.num_of_x)
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ScalarDynamicArray_HPP */
