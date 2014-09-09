#include "ScalarFixedArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
ScalarFixedArray* swap<ScalarFixedArray>(ScalarFixedArray* payload)
{
    swap_n_fixed(payload->a, 3);
    return payload + 1;
}

} // namespace raw
} // namespace prophy
