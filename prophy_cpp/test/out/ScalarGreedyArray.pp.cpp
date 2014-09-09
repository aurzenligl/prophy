#include "ScalarGreedyArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
ScalarGreedyArray* swap<ScalarGreedyArray>(ScalarGreedyArray* payload)
{
    swap(&payload->x);
    return cast<ScalarGreedyArray*>(payload->y);
}

} // namespace raw
} // namespace prophy
