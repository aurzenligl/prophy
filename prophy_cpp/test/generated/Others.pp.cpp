#include "Others.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include <prophy/detail/printer.hpp>
#include <prophy/detail/align.hpp>

namespace prophy
{
namespace detail
{

template <>
struct print_traits<Enum>
{
    static const char* to_literal(Enum x)
    {
        switch(x)
        {
            case Enum_One: return "Enum_One";
            default: return "N/A";
        }
    }
};

template <>
template <endianness E>
uint8_t* message_impl<ConstantTypedefEnum>::encode(const ConstantTypedefEnum& x, uint8_t* pos)
{
    pos = do_encode<E>(pos, x.a, 3);
    pos = do_encode<E>(pos, x.b);
    pos = do_encode<E>(pos, x.c);
    return pos;
}
template uint8_t* message_impl<ConstantTypedefEnum>::encode<native>(const ConstantTypedefEnum& x, uint8_t* pos);
template uint8_t* message_impl<ConstantTypedefEnum>::encode<little>(const ConstantTypedefEnum& x, uint8_t* pos);
template uint8_t* message_impl<ConstantTypedefEnum>::encode<big>(const ConstantTypedefEnum& x, uint8_t* pos);

template <>
template <endianness E>
bool message_impl<ConstantTypedefEnum>::decode(ConstantTypedefEnum& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.a, 3, pos, end) &&
        do_decode<E>(x.b, pos, end) &&
        do_decode<E>(x.c, pos, end)
    );
}
template bool message_impl<ConstantTypedefEnum>::decode<native>(ConstantTypedefEnum& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ConstantTypedefEnum>::decode<little>(ConstantTypedefEnum& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<ConstantTypedefEnum>::decode<big>(ConstantTypedefEnum& x, const uint8_t*& pos, const uint8_t* end);

template <>
void message_impl<ConstantTypedefEnum>::print(const ConstantTypedefEnum& x, std::ostream& out, size_t indent)
{
    do_print(out, indent, "a", x.a, 3);
    do_print(out, indent, "b", x.b);
    do_print(out, indent, "c", x.c);
}
template void message_impl<ConstantTypedefEnum>::print(const ConstantTypedefEnum& x, std::ostream& out, size_t indent);

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
bool message_impl<Floats>::decode(Floats& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.a, pos, end) &&
        do_decode_advance(4, pos, end) &&
        do_decode<E>(x.b, pos, end)
    );
}
template bool message_impl<Floats>::decode<native>(Floats& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Floats>::decode<little>(Floats& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<Floats>::decode<big>(Floats& x, const uint8_t*& pos, const uint8_t* end);

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
bool message_impl<BytesFixed>::decode(BytesFixed& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode<E>(x.x, 3, pos, end)
    );
}
template bool message_impl<BytesFixed>::decode<native>(BytesFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesFixed>::decode<little>(BytesFixed& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesFixed>::decode<big>(BytesFixed& x, const uint8_t*& pos, const uint8_t* end);

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
bool message_impl<BytesDynamic>::decode(BytesDynamic& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end) &&
        do_decode<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_align<4>(pos, end)
    );
}
template bool message_impl<BytesDynamic>::decode<native>(BytesDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesDynamic>::decode<little>(BytesDynamic& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesDynamic>::decode<big>(BytesDynamic& x, const uint8_t*& pos, const uint8_t* end);

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
bool message_impl<BytesLimited>::decode(BytesLimited& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_resize<E, uint32_t>(x.x, pos, end, 4) &&
        do_decode_in_place<E>(x.x.data(), x.x.size(), pos, end) &&
        do_decode_advance(4, pos, end)
    );
}
template bool message_impl<BytesLimited>::decode<native>(BytesLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesLimited>::decode<little>(BytesLimited& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesLimited>::decode<big>(BytesLimited& x, const uint8_t*& pos, const uint8_t* end);

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

template <>
template <endianness E>
bool message_impl<BytesGreedy>::decode(BytesGreedy& x, const uint8_t*& pos, const uint8_t* end)
{
    return (
        do_decode_greedy<E>(x.x, pos, end)
    );
}
template bool message_impl<BytesGreedy>::decode<native>(BytesGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesGreedy>::decode<little>(BytesGreedy& x, const uint8_t*& pos, const uint8_t* end);
template bool message_impl<BytesGreedy>::decode<big>(BytesGreedy& x, const uint8_t*& pos, const uint8_t* end);

} // namespace detail
} // namespace prophy
