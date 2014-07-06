#ifndef _PROPHY_GENERATED_ManyDynamic_HPP
#define _PROPHY_GENERATED_ManyDynamic_HPP

#include <prophy/prophy.hpp>

struct ManyDynamicHelper
{
    uint32_t num_of_x;
    uint16_t x[1];
};

struct ManyDynamic
{
    ManyDynamicHelper x;

    struct part2
    {
        ManyDynamicHelper y;
    } _2;

    struct part3
    {
        ManyDynamicHelper z;
    } _3;
};

#endif  /* _PROPHY_GENERATED_ManyDynamic_HPP */
