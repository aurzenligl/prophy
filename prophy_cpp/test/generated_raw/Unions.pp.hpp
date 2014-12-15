#ifndef _PROPHY_GENERATED_Unions_HPP
#define _PROPHY_GENERATED_Unions_HPP

#include <prophy/prophy.hpp>

#include "Arrays.pp.hpp"

struct Optional
{
    prophy::bool_t has_x;
    uint32_t x;
    prophy::bool_t has_y;
    Fixcomp y;
};

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
        Fixcomp c;
    };
};

namespace prophy
{

template <> Optional* swap<Optional>(Optional*);
template <> Union* swap<Union>(Union*);

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Unions_HPP */
