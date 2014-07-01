#ifndef _PROPHY_GENERATED_Optional_HPP
#define _PROPHY_GENERATED_Optional_HPP

#include <prophy/prophy.hpp>

#include "Composite.hpp"

struct Optional
{
    prophy::bool_t has_x;
    uint32_t x;
    prophy::bool_t has_y;
    Composite y;
};

namespace prophy
{

template <>
inline Optional* swap<Optional>(Optional* payload)
{
    swap(&payload->has_x);
    if (payload->has_x)
    {
        swap(&payload->x);
    }
    swap(&payload->has_y);
    if (payload->has_y)
    {
        swap(&payload->y);
    }
    return payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Optional_HPP */
