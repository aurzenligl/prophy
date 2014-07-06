#include "Composite.pp.hpp"

namespace prophy
{

template <>
Composite* swap<Composite>(Composite* payload)
{
    swap(&payload->a);
    swap(&payload->b);
    return payload + 1;
}

} // namespace prophy
