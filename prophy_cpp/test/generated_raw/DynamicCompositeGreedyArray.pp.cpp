#include "DynamicCompositeGreedyArray.pp.hpp"

namespace prophy
{

template <>
DynamicCompositeGreedyArray* swap<DynamicCompositeGreedyArray>(DynamicCompositeGreedyArray* payload)
{
    swap(&payload->x);
    return cast<DynamicCompositeGreedyArray*>(payload->y);
}

} // namespace prophy
