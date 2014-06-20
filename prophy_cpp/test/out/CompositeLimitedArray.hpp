#ifndef _PROPHY_GENERATED_CompositeLimitedArray_HPP
#define _PROPHY_GENERATED_CompositeLimitedArray_HPP

#include <prophy/prophy.hpp>

#include "Scalar.hpp"

struct CompositeLimitedArray
{
    uint16_t num_of_x;
    Scalar x[3];
};

namespace prophy
{

template <>
inline CompositeLimitedArray* swap<CompositeLimitedArray>(CompositeLimitedArray* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_CompositeLimitedArray_HPP */
