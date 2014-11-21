#ifndef _PROPHY_DETAIL_BYTE_SIZE_HPP
#define _PROPHY_DETAIL_BYTE_SIZE_HPP

namespace prophy
{
namespace detail
{

struct byte_size
{
    template <class T>
    size_t operator()(size_t x, const T& y)
    {
        return x + y.get_byte_size();
    }
};

template <size_t N, typename T>
inline T nearest(T x)
{
    return (x + N - 1) & ~T(N - 1);
}

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_BYTE_SIZE_HPP */
