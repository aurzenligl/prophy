#include "Composite.pp.hpp"

namespace prophy
{
namespace raw
{

template <>
Composite* swap<Composite>(Composite* payload)
{
    swap(&payload->a);
    swap(&payload->b);
    return payload + 1;
}

} // namespace raw
} // namespace prophy
