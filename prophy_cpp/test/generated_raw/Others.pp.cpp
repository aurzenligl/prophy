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
    swap(&payload->c);
    return payload + 1;
}

} // namespace prophy
