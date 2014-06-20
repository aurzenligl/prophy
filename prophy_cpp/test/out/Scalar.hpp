#ifndef _PROPHY_GENERATED_Scalar_HPP
#define _PROPHY_GENERATED_Scalar_HPP

#include <prophy/prophy.hpp>

struct Scalar
{
    uint8_t a;
    uint16_t b;
};

namespace prophy
{

template <>
inline Scalar* swap<Scalar>(Scalar& payload)
{
    swap(payload.a);
    swap(payload.b);
    return &payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Scalar_HPP */
