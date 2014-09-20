#include "Others.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

namespace prophy
{
namespace detail
{

template <>
template <endianness E>
uint8_t* message_impl<ConstantTypedefEnum>::encode(const ConstantTypedefEnum& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.a, 3);
    pos = do_encode<E>(pos, x.b);
    pos = do_encode<E>(pos, uint32_t(x.c));
    return pos;
}
template uint8_t* message_impl<ConstantTypedefEnum>::encode<native>(const ConstantTypedefEnum& x, uint8_t* pos);
template uint8_t* message_impl<ConstantTypedefEnum>::encode<little>(const ConstantTypedefEnum& x, uint8_t* pos);
template uint8_t* message_impl<ConstantTypedefEnum>::encode<big>(const ConstantTypedefEnum& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<Floats>::encode(const Floats& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.a);
    pos = pos + 4;
    pos = do_encode<E>(pos, x.b);
    return pos;
}
template uint8_t* message_impl<Floats>::encode<native>(const Floats& x, uint8_t* pos);
template uint8_t* message_impl<Floats>::encode<little>(const Floats& x, uint8_t* pos);
template uint8_t* message_impl<Floats>::encode<big>(const Floats& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<BytesFixed>::encode(const BytesFixed& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x, 3);
    return pos;
}
template uint8_t* message_impl<BytesFixed>::encode<native>(const BytesFixed& x, uint8_t* pos);
template uint8_t* message_impl<BytesFixed>::encode<little>(const BytesFixed& x, uint8_t* pos);
template uint8_t* message_impl<BytesFixed>::encode<big>(const BytesFixed& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<BytesDynamic>::encode(const BytesDynamic& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(x.x.size()));
    pos = do_encode<E>(pos, x.x.data(), uint32_t(x.x.size()));
    pos = align<4>(pos);
    return pos;
}
template uint8_t* message_impl<BytesDynamic>::encode<native>(const BytesDynamic& x, uint8_t* pos);
template uint8_t* message_impl<BytesDynamic>::encode<little>(const BytesDynamic& x, uint8_t* pos);
template uint8_t* message_impl<BytesDynamic>::encode<big>(const BytesDynamic& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<BytesLimited>::encode(const BytesLimited& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, uint32_t(std::min(x.x.size(), size_t(4))));
    do_encode<E>(pos, x.x.data(), std::min(x.x.size(), size_t(4)));
    pos = pos + 4;
    return pos;
}
template uint8_t* message_impl<BytesLimited>::encode<native>(const BytesLimited& x, uint8_t* pos);
template uint8_t* message_impl<BytesLimited>::encode<little>(const BytesLimited& x, uint8_t* pos);
template uint8_t* message_impl<BytesLimited>::encode<big>(const BytesLimited& x, uint8_t* pos);

template <>
template <endianness E>
uint8_t* message_impl<BytesGreedy>::encode(const BytesGreedy& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.x.data(), x.x.size());
    return pos;
}
template uint8_t* message_impl<BytesGreedy>::encode<native>(const BytesGreedy& x, uint8_t* pos);
template uint8_t* message_impl<BytesGreedy>::encode<little>(const BytesGreedy& x, uint8_t* pos);
template uint8_t* message_impl<BytesGreedy>::encode<big>(const BytesGreedy& x, uint8_t* pos);

} // namespace detail
} // namespace prophy
