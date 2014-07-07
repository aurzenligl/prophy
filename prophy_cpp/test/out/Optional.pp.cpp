#include "Optional.pp.hpp"

namespace prophy
{

template <>
Optional* swap<Optional>(Optional* payload)
{
    swap(&payload->has_x);
    if (payload->has_x) swap(&payload->x);
    swap(&payload->has_y);
    if (payload->has_y) swap(&payload->y);
    return payload + 1;
}

} // namespace prophy
