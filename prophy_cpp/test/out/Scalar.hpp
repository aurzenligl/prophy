#ifndef _PROPHY_GENERATED_Scalar_HPP
#define _PROPHY_GENERATED_Scalar_HPP

#include <prophy/prophy.hpp>

struct Scalar
{
    uint8_t a;
    uint32_t b;
    uint8_t c;
    uint16_t d;
};

namespace prophy
{

inline Scalar* swap(Scalar& payload)
{
    swap(payload.a);
    swap(payload.b);
    swap(payload.c);
    swap(payload.d);
    return &payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Scalar_HPP */
