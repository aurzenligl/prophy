#ifndef _PROPHY_GENERATED_CompositeGreedyArray_HPP
#define _PROPHY_GENERATED_CompositeGreedyArray_HPP

#include <prophy/prophy.hpp>

#include "Scalar.hpp"

struct CompositeGreedyArray
{
    uint16_t x;
    Scalar y[1];
};

namespace prophy
{

inline CompositeGreedyArray* swap(CompositeGreedyArray& payload)
{
    swap(payload.x);
    return cast<CompositeGreedyArray*>(payload.y);
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_CompositeGreedyArray_HPP */
