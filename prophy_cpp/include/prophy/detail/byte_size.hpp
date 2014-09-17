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

} // namespace detail
} // namespace prophy

#endif  /* _PROPHY_DETAIL_BYTE_SIZE_HPP */
