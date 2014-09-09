#include "DynamicCompositeGreedyArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
DynamicCompositeGreedyArray* swap<DynamicCompositeGreedyArray>(DynamicCompositeGreedyArray* payload)
{
    swap(&payload->x);
    return cast<DynamicCompositeGreedyArray*>(payload->y);
}

} // namespace raw
} // namespace prophy
