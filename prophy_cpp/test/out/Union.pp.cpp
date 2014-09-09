#include "Union.pp.hpp"

namespace prophy
{
namespace raw
{

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

} // namespace raw
} // namespace prophy
