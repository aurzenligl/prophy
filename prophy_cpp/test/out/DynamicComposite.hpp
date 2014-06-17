#ifndef _PROPHY_GENERATED_DynamicComposite_HPP
#define _PROPHY_GENERATED_DynamicComposite_HPP

#include <prophy/prophy.hpp>

struct DynamicComposite
{
    uint32_t num_of_x;
    uint16_t x[1];
};

namespace prophy
{

inline DynamicComposite* swap(DynamicComposite& payload)
{
    swap(payload.num_of_x);
    return cast<DynamicComposite*>(
        swap_n_fixed(payload.x, payload.num_of_x));
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_DynamicComposite_HPP */
