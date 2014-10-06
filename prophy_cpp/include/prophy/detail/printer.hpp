#ifndef _PROPHY_DETAIL_PRINTER_HPP_
#define _PROPHY_DETAIL_PRINTER_HPP_

#include <prophy/detail/codec_traits.hpp>

namespace prophy
{
namespace detail
{

template <typename T, bool = codec_traits<T>::is_composite>
struct printer;

template <typename T>
struct printer<T, false>
{
    static void print(std::ostream& out, const char* name, const T& x)
    {
        out << name << ": " << x << '\n';
    }

    static void print(std::ostream& out, const char* name, const T* x, size_t n)
    {
        while(n)
        {
            print(out, name, *x);
            ++x;
            --n;
        }
    }
};

template <typename T>
inline void do_print(std::ostream& out, const char* name, const T& x)
{
    printer<T>::print(out, name, x);
}

template <typename T>
inline void do_print(std::ostream& out, const char* name, const T* x, size_t n)
{
    printer<T>::print(out, name, x, n);
}

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_PRINTER_HPP_ */
