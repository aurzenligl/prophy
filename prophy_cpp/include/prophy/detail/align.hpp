#ifndef _PROPHY_DETAIL_ALIGN_HPP
#define _PROPHY_DETAIL_ALIGN_HPP

#include <stdint.h>

namespace prophy
{
namespace detail
{

template <typename Tp>
struct alignment
{
    struct finder
    {
        char align;
        Tp t;
    };
    enum { value = sizeof(finder) - sizeof(Tp) };
};

template <typename Tp>
inline Tp* align(Tp* ptr)
{
    enum { mask = alignment<Tp>::value - 1 };
    return reinterpret_cast<Tp*>((reinterpret_cast<uintptr_t>(ptr) + mask) & ~uintptr_t(mask));
}

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_ALIGN_HPP */
