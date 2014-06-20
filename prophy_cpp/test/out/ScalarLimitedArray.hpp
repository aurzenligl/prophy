#ifndef _PROPHY_GENERATED_ScalarLimitedArray_HPP
#define _PROPHY_GENERATED_ScalarLimitedArray_HPP

#include <prophy/prophy.hpp>

struct ScalarLimitedArray
{
    uint32_t num_of_x;
    uint16_t x[3];
};

namespace prophy
{

template <>
inline ScalarLimitedArray* swap<ScalarLimitedArray>(ScalarLimitedArray& payload)
{
    swap(payload.num_of_x);
    swap_n_fixed(payload.x, payload.num_of_x);
    return &payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ScalarLimitedArray_HPP */
