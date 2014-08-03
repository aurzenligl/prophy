#ifndef _PROPHY_GENERATED_Union_HPP
#define _PROPHY_GENERATED_Union_HPP

#include <prophy/prophy.hpp>

#include "Composite.pp.hpp"

struct Union
{
    enum _discriminator
    {
        discriminator_a = 1,
        discriminator_b = 2,
        discriminator_c = 3
    } discriminator;

    union
    {
        uint8_t a;
        uint64_t b;
        Composite c;
    };
};

#endif  /* _PROPHY_GENERATED_Union_HPP */
