#ifndef _PROPHY_GENERATED_DynamicCompositeComposite_HPP
#define _PROPHY_GENERATED_DynamicCompositeComposite_HPP

#include <prophy/prophy.hpp>

#include "DynamicComposite.hpp"

struct DynamicCompositeComposite
{
    DynamicComposite x;

    struct part2
    {
        uint32_t y;
        DynamicComposite z[2];
    } _2;
};

namespace prophy
{

inline DynamicCompositeComposite::part2* swap(DynamicCompositeComposite::part2* payload)
{
    swap(&payload->y);
    return cast<DynamicCompositeComposite::part2*>(swap_n_dynamic(payload->z, 2));
}

template <>
inline DynamicCompositeComposite* swap<DynamicCompositeComposite>(DynamicCompositeComposite* payload)
{
    DynamicCompositeComposite::part2* part2 = cast<DynamicCompositeComposite::part2*>(swap(&payload->x));
    return cast<DynamicCompositeComposite*>(swap(part2));
}

} // namespace prophy

#endif  /* _PROPHY_GENERATED_DynamicCompositeComposite_HPP */
