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

template <int I>
struct int2type
{
    enum { value = I };
};

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_MPL_HPP */
