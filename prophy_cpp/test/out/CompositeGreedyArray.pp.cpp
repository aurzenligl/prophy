#include "CompositeGreedyArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
CompositeGreedyArray* swap<CompositeGreedyArray>(CompositeGreedyArray* payload)
{
    swap(&payload->x);
    return cast<CompositeGreedyArray*>(payload->y);
}

} // namespace raw
} // namespace prophy
