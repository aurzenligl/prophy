#ifndef _PROPHY_RAW_DETAIL_UTILS_HPP
#define _PROPHY_RAW_DETAIL_UTILS_HPP

#include <stdint.h>

namespace prophy
{
namespace raw
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

template <class T, class U>
class is_convertible
{
    class big_t { char dummy[2]; };
    static char test(U);
    static big_t test(...);
    static T make();
public:
    enum { value = sizeof(test(make())) == sizeof(char) };
};

template <bool, class T = void>
struct enable_if
{};

template <class T>
struct enable_if<true, T>
{
    typedef T type;
};

} // namespace detail
} // namespace raw
} // namespace prophy

#endif  /* _PROPHY_RAW_DETAIL_UTILS_HPP */
