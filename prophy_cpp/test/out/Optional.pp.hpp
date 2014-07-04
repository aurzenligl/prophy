#ifndef _PROPHY_GENERATED_Optional_HPP
#define _PROPHY_GENERATED_Optional_HPP

#include <prophy/prophy.hpp>

#include "Composite.pp.hpp"

struct Optional
{
    prophy::bool_t has_x;
    uint32_t x;
    prophy::bool_t has_y;
    Composite y;
};

#endif  /* _PROPHY_GENERATED_Optional_HPP */
