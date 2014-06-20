#ifndef _PROPHY_GENERATED_CompositeFixedArray_HPP
#define _PROPHY_GENERATED_CompositeFixedArray_HPP

#include <prophy/prophy.hpp>

#include "Scalar.hpp"

struct CompositeFixedArray
{
    Scalar a[3];
};

namespace prophy
{

template <>
inline CompositeFixedArray* swap<CompositeFixedArray>(CompositeFixedArray* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_CompositeFixedArray_HPP */
