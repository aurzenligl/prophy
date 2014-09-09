#ifndef _PROPHY_GENERATED_ManyArraysPadding_HPP
#define _PROPHY_GENERATED_ManyArraysPadding_HPP

#include <prophy/raw/prophy.hpp>

struct ManyArraysPaddingInner
{
    uint8_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint32_t num_of_y;
        uint8_t y[1];
    } _2;

    struct part3
    {
        uint64_t z;
    } _3;
};

struct ManyArraysPadding
{
    uint8_t x;
    ManyArraysPaddingInner y;
};

#endif  /* _PROPHY_GENERATED_ManyArraysPadding_HPP */
