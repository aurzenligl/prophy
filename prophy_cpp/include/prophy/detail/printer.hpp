#ifndef _PROPHY_DETAIL_PRINTER_HPP_
#define _PROPHY_DETAIL_PRINTER_HPP_

#include <prophy/detail/codec_traits.hpp>
#include <prophy/detail/message_impl.hpp>

namespace prophy
{
namespace detail
{

template <typename T>
struct print_traits
{
    static const char* to_literal(T x);
};

inline void print_byte(std::ostream& out, uint8_t x)
{
    switch (x)
    {
        case 9: out << "\\t"; return;
        case 10: out << "\\n"; return;
        case 13: out << "\\r"; return;
        case 92: out << "\\\\"; return;
    }
    if ((x >= 32) && (x <= 126))
    {
        out << char(x);
    }
    else
    {
        out << "\\x";
        out.width(2);
        out.fill('0');
        out << std::hex << unsigned(x);
    }
}

inline std::ostream& operator<<(std::ostream& out, int8_t x)
{
    out << int(x);
    return out;
}

inline std::ostream& operator<<(std::ostream& out, uint8_t x)
{
    out << unsigned(x);
    return out;
}

inline std::ostream& operator<<(std::ostream& out, std::pair<const uint8_t*, size_t> bytes)
{
    out << '\'';
    while (bytes.second)
    {
        print_byte(out, *bytes.first);
        ++bytes.first;
        --bytes.second;
    }
    out << '\'';
    return out;
}

template <typename T,
          bool = codec_traits<T>::is_composite,
          bool = codec_traits<T>::is_enum_or_bool>
struct printer;

template <typename T>
struct printer<T, false, false>
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
struct printer<T, false, true>
{
    static void print(std::ostream& out, size_t indent, const char* name, const T& x)
    {
        while (indent)
        {
            out << "  ";
            --indent;
        }
        const char* literal = print_traits<T>::to_literal(x);
        out << name << ": ";
        if (literal)
        {
            out << literal;
        }
        else
        {
            out << uint32_t(x);
        }
        out << '\n';
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
struct printer<T, true, false>
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
