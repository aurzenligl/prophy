#ifndef _PROPHY_GENERATED_DynamicCompositeGreedyArray_HPP
#define _PROPHY_GENERATED_DynamicCompositeGreedyArray_HPP

#include <prophy/prophy.hpp>

#include "DynamicComposite.hpp"

struct DynamicCompositeGreedyArray
{
    uint16_t x;
    DynamicComposite y[1];
};

namespace prophy
{

inline DynamicCompositeGreedyArray* swap(DynamicCompositeGreedyArray& payload)
{
    swap(payload.x);
    return cast<DynamicCompositeGreedyArray*>(
        payload.y
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_DynamicCompositeGreedyArray_HPP */
