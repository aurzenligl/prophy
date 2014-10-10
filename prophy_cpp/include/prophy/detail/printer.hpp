#ifndef _PROPHY_DETAIL_PRINTER_HPP_
#define _PROPHY_DETAIL_PRINTER_HPP_

#include <prophy/detail/codec_traits.hpp>
#include <prophy/detail/message_impl.hpp>

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

template <typename T>
struct print_traits
{
    static const T& get_value(const T& x)
    {
        return x;
    }
};

template <typename T, bool = is_class_or_union<T>::value>
struct printer;

template <typename T>
struct printer<T, false>
{
    static void print(std::ostream& out, size_t indent, const char* name, const T& x)
    {
        while (indent)
        {
            out << "  ";
            --indent;
        }
        out << name << ": " << print_traits<T>::get_value(x) << '\n';
    }

    static void print(std::ostream& out, size_t indent, const char* name, const T* x, size_t n)
    {
        while(n)
        {
            print(out, indent, name, *x);
            ++x;
            --n;
        }
    }
};

template <typename T>
struct printer<T, true>
{
    static void print(std::ostream& out, size_t indent, const char* name, const T& x)
    {
        out << name << " {\n";
        message_impl<T>::print(x, out, indent + 1);
        out << "}\n";
    }

    static void print(std::ostream& out, size_t indent, const char* name, const T* x, size_t n)
    {
        while(n)
        {
            print(out, indent, name, *x);
            ++x;
            --n;
        }
    }
};

template <typename T>
inline void do_print(std::ostream& out, size_t indent, const char* name, const T& x)
{
    printer<T>::print(out, indent, name, x);
}

template <typename T>
inline void do_print(std::ostream& out, size_t indent, const char* name, const T* x, size_t n)
{
    printer<T>::print(out, indent, name, x, n);
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_PRINTER_HPP_ */
