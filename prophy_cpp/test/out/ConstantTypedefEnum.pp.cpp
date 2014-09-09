#include "ConstantTypedefEnum.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
ConstantTypedefEnum* swap<ConstantTypedefEnum>(ConstantTypedefEnum* payload)
{
    swap_n_fixed(payload->a, CONSTANT);
    swap(&payload->b);
    swap(&payload->c);
    return payload + 1;
}

} // namespace raw
} // namespace prophy
