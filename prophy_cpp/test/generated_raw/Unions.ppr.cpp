#include "Unions.ppr.hpp"

using namespace raw;

namespace prophy
{

template <>
Optional* swap<Optional>(Optional* payload)
{
    swap(&payload->has_x);
    if (payload->has_x) swap(&payload->x);
    swap(&payload->has_y);
    if (payload->has_y) swap(&payload->y);
    return payload + 1;
}

template <>
Union* swap<Union>(Union* payload)
{
    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
    switch (payload->discriminator)
    {
        case Union::discriminator_a: swap(&payload->a); break;
        case Union::discriminator_b: swap(&payload->b); break;
        case Union::discriminator_c: swap(&payload->c); break;
        default: break;
    }
    return payload + 1;
}

} // namespace prophy
