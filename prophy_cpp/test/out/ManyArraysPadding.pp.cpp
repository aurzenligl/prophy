#include "ManyArraysPadding.pp.hpp"

namespace prophy
{

inline ManyArraysPaddingInner::part2* swap(ManyArraysPaddingInner::part2* payload)
{
    swap(&payload->num_of_y);
    return cast<ManyArraysPaddingInner::part2*>(swap_n_fixed(payload->y, payload->num_of_y));
}

inline ManyArraysPaddingInner::part3* swap(ManyArraysPaddingInner::part3* payload)
{
    swap(&payload->z);
    return payload + 1;
}

template <>
ManyArraysPaddingInner* swap<ManyArraysPaddingInner>(ManyArraysPaddingInner* payload)
{
    swap(&payload->num_of_x);
    ManyArraysPaddingInner::part2* part2 = cast<ManyArraysPaddingInner::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    ManyArraysPaddingInner::part3* part3 = cast<ManyArraysPaddingInner::part3*>(swap(part2));
    return cast<ManyArraysPaddingInner*>(swap(part3));
}

template <>
ManyArraysPadding* swap<ManyArraysPadding>(ManyArraysPadding* payload)
{
    swap(&payload->x);
    return cast<ManyArraysPadding*>(swap(&payload->y));
}

} // namespace prophy
