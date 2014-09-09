#include "ScalarGreedyArray.pp.hpp"

namespace prophy
{

template <>
ScalarGreedyArray* swap<ScalarGreedyArray>(ScalarGreedyArray* payload)
{
    swap(&payload->x);
    return cast<ScalarGreedyArray*>(payload->y);
}

} // namespace prophy
