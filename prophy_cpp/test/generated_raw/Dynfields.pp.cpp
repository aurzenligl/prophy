#include "Dynfields.pp.hpp"

namespace prophy
{

inline Dynfields::part2* swap(Dynfields::part2* payload)
{
    swap(&payload->num_of_y);
    return cast<Dynfields::part2*>(swap_n_fixed(payload->y, payload->num_of_y));
}

inline Dynfields::part3* swap(Dynfields::part3* payload)
{
    swap(&payload->num_of_z);
    return cast<Dynfields::part3*>(swap_n_fixed(payload->z, payload->num_of_z));
}

template <>
Dynfields* swap<Dynfields>(Dynfields* payload)
{
    swap(&payload->num_of_x);
    Dynfields::part2* part2 = cast<Dynfields::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    Dynfields::part3* part3 = cast<Dynfields::part3*>(swap(part2));
    return cast<Dynfields*>(swap(part3));
}

inline DynfieldsMixed::part2* swap(DynfieldsMixed::part2* payload, size_t num_of_y)
{
    return cast<DynfieldsMixed::part2*>(swap_n_fixed(payload->y, num_of_y));
}

template <>
DynfieldsMixed* swap<DynfieldsMixed>(DynfieldsMixed* payload)
{
    swap(&payload->num_of_x);
    swap(&payload->num_of_y);
    DynfieldsMixed::part2* part2 = cast<DynfieldsMixed::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<DynfieldsMixed*>(swap(part2, payload->num_of_y));
}

inline DynfieldsOverlapped::part2* swap(DynfieldsOverlapped::part2* payload)
{
    swap(&payload->num_of_c);
    return cast<DynfieldsOverlapped::part2*>(swap_n_fixed(payload->c, payload->num_of_c));
}

inline DynfieldsOverlapped::part3* swap(DynfieldsOverlapped::part3* payload, size_t num_of_a)
{
    return cast<DynfieldsOverlapped::part3*>(swap_n_fixed(payload->a, num_of_a));
}

template <>
DynfieldsOverlapped* swap<DynfieldsOverlapped>(DynfieldsOverlapped* payload)
{
    swap(&payload->num_of_a);
    swap(&payload->num_of_b);
    DynfieldsOverlapped::part2* part2 = cast<DynfieldsOverlapped::part2*>(swap_n_fixed(payload->b, payload->num_of_b));
    DynfieldsOverlapped::part3* part3 = cast<DynfieldsOverlapped::part3*>(swap(part2));
    return cast<DynfieldsOverlapped*>(swap(part3, payload->num_of_a));
}

inline DynfieldsPadded_Helper::part2* swap(DynfieldsPadded_Helper::part2* payload)
{
    swap(&payload->num_of_y);
    return cast<DynfieldsPadded_Helper::part2*>(swap_n_fixed(payload->y, payload->num_of_y));
}

inline DynfieldsPadded_Helper::part3* swap(DynfieldsPadded_Helper::part3* payload)
{
    swap(&payload->z);
    return payload + 1;
}

template <>
DynfieldsPadded_Helper* swap<DynfieldsPadded_Helper>(DynfieldsPadded_Helper* payload)
{
    swap(&payload->num_of_x);
    DynfieldsPadded_Helper::part2* part2 = cast<DynfieldsPadded_Helper::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    DynfieldsPadded_Helper::part3* part3 = cast<DynfieldsPadded_Helper::part3*>(swap(part2));
    return cast<DynfieldsPadded_Helper*>(swap(part3));
}

template <>
DynfieldsPadded* swap<DynfieldsPadded>(DynfieldsPadded* payload)
{
    swap(&payload->x);
    return cast<DynfieldsPadded*>(swap(&payload->y));
}

inline DynfieldsFixtail::part2* swap(DynfieldsFixtail::part2* payload)
{
    swap(&payload->y);
    swap(&payload->z);
    return payload + 1;
}

template <>
DynfieldsFixtail* swap<DynfieldsFixtail>(DynfieldsFixtail* payload)
{
    swap(&payload->num_of_x);
    DynfieldsFixtail::part2* part2 = cast<DynfieldsFixtail::part2*>(swap_n_fixed(payload->x, payload->num_of_x));
    return cast<DynfieldsFixtail*>(swap(part2));
}

inline DynfieldsComp::part2* swap(DynfieldsComp::part2* payload)
{
    return cast<DynfieldsComp::part2*>(swap(&payload->y));
}

inline DynfieldsComp::part3* swap(DynfieldsComp::part3* payload)
{
    return cast<DynfieldsComp::part3*>(swap(&payload->z));
}

template <>
DynfieldsComp* swap<DynfieldsComp>(DynfieldsComp* payload)
{
    DynfieldsComp::part2* part2 = cast<DynfieldsComp::part2*>(swap(&payload->x));
    DynfieldsComp::part3* part3 = cast<DynfieldsComp::part3*>(swap(part2));
    return cast<DynfieldsComp*>(swap(part3));
}

} // namespace prophy
