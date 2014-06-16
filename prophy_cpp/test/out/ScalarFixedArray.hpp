#ifndef _PROPHY_GENERATED_ScalarFixedArray_HPP
#define _PROPHY_GENERATED_ScalarFixedArray_HPP

#include <prophy/prophy.hpp>

#include "Scalar.hpp"

struct ScalarFixedArray
{
    Scalar a[3];
};

namespace prophy
{

inline ScalarFixedArray* swap(ScalarFixedArray& payload)
{
    swap_n_fixed(payload.a, 3);
    return &payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_ScalarFixedArray_HPP */
