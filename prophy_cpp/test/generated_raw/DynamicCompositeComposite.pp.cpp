#include "DynamicCompositeComposite.pp.hpp"

namespace prophy
{

inline DynamicCompositeComposite::part2* swap(DynamicCompositeComposite::part2* payload)
{
    swap(&payload->y);
    return cast<DynamicCompositeComposite::part2*>(swap_n_dynamic(payload->z, 2));
}

template <>
DynamicCompositeComposite* swap<DynamicCompositeComposite>(DynamicCompositeComposite* payload)
{
    DynamicCompositeComposite::part2* part2 = cast<DynamicCompositeComposite::part2*>(swap(&payload->x));
    return cast<DynamicCompositeComposite*>(swap(part2));
}

} // namespace prophy
