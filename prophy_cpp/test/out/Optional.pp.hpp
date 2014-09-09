#ifndef _PROPHY_GENERATED_Optional_HPP
#define _PROPHY_GENERATED_Optional_HPP

#include <prophy/raw/prophy.hpp>

#include "Composite.pp.hpp"

struct Optional
{
    prophy::raw::bool_t has_x;
    uint32_t x;
    prophy::raw::bool_t has_y;
    Composite y;
};

#endif  /* _PROPHY_GENERATED_Optional_HPP */
