#include "DynamicComposite.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
DynamicCompositeInner* swap<DynamicCompositeInner>(DynamicCompositeInner* payload)
{
    swap(&payload->num_of_x);
    return cast<DynamicCompositeInner*>(swap_n_fixed(payload->x, payload->num_of_x));
}

template <>
DynamicComposite* swap<DynamicComposite>(DynamicComposite* payload)
{
    return cast<DynamicComposite*>(swap(&payload->x));
}

} // namespace raw
} // namespace prophy
