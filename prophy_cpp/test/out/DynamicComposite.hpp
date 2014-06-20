#ifndef _PROPHY_GENERATED_DynamicComposite_HPP
#define _PROPHY_GENERATED_DynamicComposite_HPP

#include <prophy/prophy.hpp>

struct DynamicCompositeInner
{
    uint32_t num_of_x;
    uint16_t x[1];
};

struct DynamicComposite
{
    DynamicCompositeInner x;
};

namespace prophy
{

template <>
inline DynamicCompositeInner* swap<DynamicCompositeInner>(DynamicCompositeInner* payload)
{
    swap(&payload->num_of_x);
    return cast<DynamicCompositeInner*>(
        swap_n_fixed(payload->x, payload->num_of_x)
    );
}

template <>
inline DynamicComposite* swap<DynamicComposite>(DynamicComposite* payload)
{
    return cast<DynamicComposite*>(
        swap(&payload->x)
    );
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_DynamicComposite_HPP */
