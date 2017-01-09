#ifndef _PROPHY_DETAIL_STRUCT_HPP
#define _PROPHY_DETAIL_STRUCT_HPP

#include <stddef.h>
#include <prophy/prophy.hpp>

namespace prophy
{
namespace detail
{

#if defined(__GNUC__) || defined(__TMS320C6X__)
    #define PROPHY_STRUCT(alignment) struct __attribute__((aligned(alignment), packed))
#else
    #error "Unknown compiler, cannot set aligned/packed attributes/pragmas"
#endif

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_STRUCT_HPP */
