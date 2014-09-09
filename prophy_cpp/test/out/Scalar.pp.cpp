#include "Scalar.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
Scalar* swap<Scalar>(Scalar* payload)
{
    swap(&payload->a);
    swap(&payload->b);
    return payload + 1;
}

} // namespace raw
} // namespace prophy
