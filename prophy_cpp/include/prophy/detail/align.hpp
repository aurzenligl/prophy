#ifndef _PROPHY_DETAIL_ALIGN_HPP
#define _PROPHY_DETAIL_ALIGN_HPP

#include <stddef.h>
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
inline Tp* align_ptr(Tp* ptr)
{
    enum { mask = alignment<Tp>::value - 1 };
    return reinterpret_cast<Tp*>((reinterpret_cast<uintptr_t>(ptr) + mask) & ~uintptr_t(mask));
}

template <size_t Alignment>
inline uint8_t* align(uint8_t* ptr)
{
    enum { mask = Alignment - 1 };
    return reinterpret_cast<uint8_t*>((reinterpret_cast<uintptr_t>(ptr) + mask) & ~uintptr_t(mask));
}

template <size_t Alignment>
inline const uint8_t* align(const uint8_t* ptr)
{
    return align<Alignment>(const_cast<uint8_t*>(ptr));
}

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_ALIGN_HPP */
