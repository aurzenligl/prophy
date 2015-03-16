#ifndef _PROPHY_DETAIL_MPL_HPP
#define _PROPHY_DETAIL_MPL_HPP

namespace prophy
{
namespace detail
{

template<class T>
struct is_class_or_union
{
    struct twochar { char _[2]; };
    template <class U>
    static char is_class_or_union_tester(void(U::*)(void));
    template <class U>
    static twochar is_class_or_union_tester(...);
    static const bool value = sizeof(is_class_or_union_tester<T>(0)) == sizeof(char);
};

template <int I>
struct int2type
{
    enum { value = I };
};

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_MPL_HPP */
