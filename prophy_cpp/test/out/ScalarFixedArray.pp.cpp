#include "ScalarFixedArray.pp.hpp"

namespace prophy
{

template <>
ScalarFixedArray* swap<ScalarFixedArray>(ScalarFixedArray* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

} // namespace prophy
