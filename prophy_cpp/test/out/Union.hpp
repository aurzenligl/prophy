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

namespace prophy
{

template <>
inline Union* swap<Union>(Union* payload)
{
    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
    switch (payload->discriminator)
    {
        case Union::discriminator_a: swap(&payload->a); break;
        case Union::discriminator_b: swap(&payload->b); break;
        case Union::discriminator_c: swap(&payload->c); break;
        default: break;
    }
    return payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Union_HPP */
