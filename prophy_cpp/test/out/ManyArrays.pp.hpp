#ifndef _PROPHY_GENERATED_ManyArrays_HPP
#define _PROPHY_GENERATED_ManyArrays_HPP

#include <prophy/raw/prophy.hpp>

struct ManyArrays
{
    uint32_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint16_t num_of_y;
        uint16_t y[1];
    } _2;

    struct part3
    {
        uint8_t num_of_z;
        uint64_t z[1];
    } _3;
};

#endif  /* _PROPHY_GENERATED_ManyArrays_HPP */
