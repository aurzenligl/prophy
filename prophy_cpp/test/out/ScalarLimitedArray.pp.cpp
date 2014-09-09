#include "ScalarLimitedArray.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
ScalarLimitedArray* swap<ScalarLimitedArray>(ScalarLimitedArray* payload)
{
    swap(&payload->num_of_x);
    swap_n_fixed(payload->x, payload->num_of_x);
    return payload + 1;
}

} // namespace raw
} // namespace prophy
