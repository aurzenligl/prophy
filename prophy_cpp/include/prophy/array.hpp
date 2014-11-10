/* The following code declares class array,
 * an STL container (as wrapper) for arrays of constant size.
 *
 * See
 *      http://www.boost.org/libs/array/
 * for documentation.
 *
 * The original author site is at: http://www.josuttis.com/
 *
 * (C) Copyright Nicolai M. Josuttis 2001.
 *
 * Distributed under the Boost Software License, Version 1.0. (See
 * accompanying file LICENSE_1_0.txt or copy at
 * http://www.boost.org/LICENSE_1_0.txt)
 */

#ifndef _PROPHY_ARRAY_HPP_
#define _PROPHY_ARRAY_HPP_

#include <cstddef>
#include <algorithm>

namespace prophy
{

template <class T, std::size_t N>
struct array
{
    T elems[N];    // fixed-size array of elements of type T

    // type definitions
    typedef T              value_type;
    typedef T*             iterator;
    typedef const T*       const_iterator;
    typedef T&             reference;
    typedef const T&       const_reference;
    typedef std::size_t    size_type;
    typedef std::ptrdiff_t difference_type;

    // iterator support
    iterator        begin()       { return elems; }
    const_iterator  begin() const { return elems; }
    const_iterator cbegin() const { return elems; }

    iterator        end()       { return elems+N; }
    const_iterator  end() const { return elems+N; }
    const_iterator cend() const { return elems+N; }

    // operator[]
    reference operator[](size_type i)
    {
        return elems[i];
    }

    const_reference operator[](size_type i) const
    {
        return elems[i];
    }

    // front() and back()
    reference front()
    {
        return elems[0];
    }

    const_reference front() const
    {
        return elems[0];
    }

    reference back()
    {
        return elems[N-1];
    }

    const_reference back() const
    {
        return elems[N-1];
    }

    static size_type size() { return N; }
    static bool empty() { return false; }
    static size_type max_size() { return N; }
    enum { static_size = N };

    // swap (note: linear complexity)
    void swap (array<T,N>& y)
    {
        for (size_type i = 0; i < N; ++i)
        {
            std::swap(elems[i], y.elems[i]);
        }
    }

    // direct access to data (read-only)
    const T* data() const { return elems; }
    T* data() { return elems; }

    // use array as C array (direct read/write access to data)
    T* c_array() { return elems; }

    // assignment with type conversion
    template <typename T2>
    array<T,N>& operator= (const array<T2, N>& rhs)
    {
        std::copy(rhs.begin(), rhs.end(), begin());
        return *this;
    }

    // assign one value to all elements
    void assign (const T& value) { fill ( value ); }    // A synonym for fill
    void fill   (const T& value)
    {
        std::fill_n(begin(),size(),value);
    }
};

// comparisons
template <class T, std::size_t N>
bool operator==(const array<T, N>& x, const array<T, N>& y)
{
    return std::equal(x.begin(), x.end(), y.begin());
}
template <class T, std::size_t N>
bool operator<(const array<T, N>& x, const array<T, N>& y)
{
    return std::lexicographical_compare(x.begin(), x.end(), y.begin(), y.end());
}
template <class T, std::size_t N>
bool operator!=(const array<T, N>& x, const array<T, N>& y)
{
    return !(x == y);
}
template <class T, std::size_t N>
bool operator>(const array<T, N>& x, const array<T, N>& y)
{
    return y < x;
}
template <class T, std::size_t N>
bool operator<=(const array<T, N>& x, const array<T, N>& y)
{
    return !(y < x);
}
template <class T, std::size_t N>
bool operator>=(const array<T, N>& x, const array<T, N>& y)
{
    return !(x < y);
}

// global swap()
template <class T, std::size_t N>
inline void swap (array<T, N>& x, array<T, N>& y)
{
    x.swap(y);
}

} // namespace prophy

#endif /* _PROPHY_ARRAY_HPP_ */
