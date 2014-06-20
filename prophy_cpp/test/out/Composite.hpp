#ifndef _PROPHY_GENERATED_Composite_HPP
#define _PROPHY_GENERATED_Composite_HPP

#include <prophy/prophy.hpp>

#include "Scalar.hpp"

struct Composite
{
    Scalar a;
    Scalar b;
};

namespace prophy
{

template <>
inline Composite* swap<Composite>(Composite* payload)
{
    swap(&payload->a);
    swap(&payload->b);
    return payload + 1;
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Composite_HPP */
