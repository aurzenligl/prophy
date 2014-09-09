#include "CompositeGreedyArray.pp.hpp"

namespace prophy
{

template <>
CompositeGreedyArray* swap<CompositeGreedyArray>(CompositeGreedyArray* payload)
{
    swap(&payload->x);
    return cast<CompositeGreedyArray*>(payload->y);
}

} // namespace prophy
