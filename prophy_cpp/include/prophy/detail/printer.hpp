#ifndef _PROPHY_DETAIL_PRINTER_HPP_
#define _PROPHY_DETAIL_PRINTER_HPP_

#include <prophy/detail/codec_traits.hpp>
#include <prophy/detail/message_impl.hpp>

namespace prophy
{
namespace detail
{

template <typename T, bool = codec_traits<T>::is_composite>
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
        out << name << ": " << x << '\n';
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
