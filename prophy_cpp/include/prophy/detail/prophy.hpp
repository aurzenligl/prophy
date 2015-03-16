#ifndef _PROPHY_DETAIL_PROPHY_HPP
#define _PROPHY_DETAIL_PROPHY_HPP

#include <stddef.h>
#include <prophy/prophy.hpp>

namespace prophy
{
namespace detail
{

template <typename Tp>
inline Tp* swap_n_fixed(Tp* first, size_t n)
{
    while (n--)
    {
        swap(first);
        ++first;
    }
    return first;
}

template <typename Tp>
inline Tp* swap_n_dynamic(Tp* first, size_t n)
{
    while (n--)
    {
        first = swap(first);
    }
    return first;
}

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_PROPHY_HPP */
