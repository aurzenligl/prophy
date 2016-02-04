#ifndef _PROPHY_DETAIL_MESSAGE_IMPL_HPP_
#define _PROPHY_DETAIL_MESSAGE_IMPL_HPP_

#include <stdint.h>
#include <string>
#include <iosfwd>
#include <prophy/endianness.hpp>
#include <prophy/detail/message.hpp>

namespace prophy
{
namespace detail
{

//template <endianness E>
//inline uint8_t* encode_scalar(const uint8_t* obj, uint8_t* pos, const field& fdsc)
//{
//    switch (fdsc.type)
//    {
//        case i8: ;
//        case i16: ;
//        case i32: ;
//        case i64: ;
//        case u8: ;
//        case u16: ;
//        case u32: ;
//        case u64: ;
//        case r32: ;
//        case r64: ;
//        case udt: pos = encode(obj, pos, *fdsc.dsc);
//    }
//}
//
//template <endianness E>
//inline uint8_t* encode_length(const uint8_t* obj, uint8_t* pos, const field& fdsc)
//{
//    sz = fdsc.access->size(obj);
//    switch (fdsc.type)
//    {
//        case u8: ;
//        case u16: ;
//        case u32: ;
//        case u64: ;
//        default:
//    }
//}
//
//template <endianness E>
//inline uint8_t* encode_vector(const uint8_t* obj, uint8_t* pos, const field& fdsc)
//{
//    sz = fdsc.access->size(obj);
//    elem = fdsc.access->elem(obj);
//    switch (fdsc.type)
//    {
//        case i8: ;
//        case i16: ;
//        case i32: ;
//        case i64: ;
//        case u8: ;
//        case u16: ;
//        case u32: ;
//        case u64: ;
//        case r32: ;
//        case r64: pos = do_encode(pos, reinterpret_cast<const r64*>(elem), sz);
//        case udt: while (sz--) { pos = encode(elem, pos, *fdsc.dsc); }
//    }
//}
//
//template <endianness E>
//inline uint8_t* encode_optional(const uint8_t* obj, uint8_t* pos, const field& fdsc)
//{
//    elem = fdsc.access->elem(obj);
//    pos = do_encode<E>(pos, uint32_t(bool(elem)));
//    align = get_alignment(fdsc.type);
//    if (align > sizeof(uint32_t))
//    {
//        pos = pos + align - sizeof(uint32_t);
//    }
//    if (elem)
//    {
//        encode_scalar(elem, pos, fdsc);
//    }
//    pos += get_size(fdsc);
//}

template <endianness E>
uint8_t* encode(const uint8_t* obj, uint8_t* pos, const descriptor& dsc)
{
//    for (auto fdsc : dsc.fields)
//    {
//        uint8_t* field = obj + fdsc.offset;
//        switch (fdsc.card)
//        {
//            case scalar: pos = encode_scalar<E>(field, pos, fdsc);
//            case length: pos = encode_length<E>(field, pos, fdsc);
//            case vector: pos = encode_vector(field, pos, fdsc);
//            case optional: pos = encode_optional(field, pos, fdsc);
//        }
//    }
    return pos;
}

template <endianness E>
bool decode(uint8_t* obj, const uint8_t*& pos, const uint8_t* end, const descriptor& dsc)
{
    return true;
}

template <typename T>
void print(const uint8_t* obj, std::ostream& out, size_t indent, const descriptor& dsc)
{ }

template uint8_t* encode<native>(const uint8_t* obj, uint8_t* pos, const descriptor& dsc);
template uint8_t* encode<little>(const uint8_t* obj, uint8_t* pos, const descriptor& dsc);
template uint8_t* encode<big>(const uint8_t* obj, uint8_t* pos, const descriptor& dsc);
template bool decode<native>(uint8_t* obj, const uint8_t*& pos, const uint8_t* end, const descriptor& dsc);
template bool decode<little>(uint8_t* obj, const uint8_t*& pos, const uint8_t* end, const descriptor& dsc);
template bool decode<big>(uint8_t* obj, const uint8_t*& pos, const uint8_t* end, const descriptor& dsc);
template void print<void>(const uint8_t* obj, std::ostream& out, size_t indent, const descriptor& dsc);

} // namespace detail
} // namespace prophy

#endif /* _PROPHY_DETAIL_MESSAGE_IMPL_HPP_ */
