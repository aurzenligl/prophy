#include <prophy/detail/prophy.hpp>

#include "Others.pp.hpp"

using namespace prophy::detail;

namespace prophy
{

template <>
ConstantTypedefEnum* swap<ConstantTypedefEnum>(ConstantTypedefEnum* payload)
{
    swap_n_fixed(payload->a, CONSTANT);
    swap(&payload->b);
    swap(reinterpret_cast<uint32_t*>(&payload->c));
    return payload + 1;
}

template <>
EnumArrays* swap<EnumArrays>(EnumArrays* payload)
{
    swap_n_fixed(reinterpret_cast<uint32_t*>(&payload->a), 2);
    swap(&payload->num_of_b);
    swap_n_fixed(reinterpret_cast<uint32_t*>(payload->b), payload->num_of_b);
    swap(&payload->num_of_c);
    return cast<EnumArrays*>(swap_n_fixed(reinterpret_cast<uint32_t*>(payload->c), payload->num_of_c));
}

template <>
EnumGreedyArray* swap<EnumGreedyArray>(EnumGreedyArray* payload)
{
    return cast<EnumGreedyArray*>(reinterpret_cast<uint32_t*>(&payload->x));
}

template <>
EnumUnion* swap<EnumUnion>(EnumUnion* payload)
{
    swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
    switch (payload->discriminator)
    {
        case EnumUnion::discriminator_x: swap(reinterpret_cast<uint32_t*>(&payload->x)); break;
        default: break;
    }
    return payload + 1;
}

} // namespace prophy
