#include "Arrays.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t Builtin::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Builtin::encode<native>(void* data) const;
template size_t Builtin::encode<little>(void* data) const;
template size_t Builtin::encode<big>(void* data) const;

template <endianness E>
const uint8_t* Builtin::decode_impl(const uint8_t* pos, const uint8_t* end)
{
    do_decode<E>(x, pos, end) &&
    do_decode<E>(y, pos, end);
    return pos;
}

template const uint8_t* Builtin::decode_impl<native>(const uint8_t* data, const uint8_t* end);
template const uint8_t* Builtin::decode_impl<little>(const uint8_t* data, const uint8_t* end);
template const uint8_t* Builtin::decode_impl<big>(const uint8_t* data, const uint8_t* end);

template <endianness E>
size_t BuiltinFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x, 2);
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinFixed::encode<native>(void* data) const;
template size_t BuiltinFixed::encode<little>(void* data) const;
template size_t BuiltinFixed::encode<big>(void* data) const;

template <endianness E>
size_t BuiltinDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinDynamic::encode<native>(void* data) const;
template size_t BuiltinDynamic::encode<little>(void* data) const;
template size_t BuiltinDynamic::encode<big>(void* data) const;

template <endianness E>
size_t BuiltinLimited::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(std::min(x.size(), size_t(2))));
    do_encode<E>(pos, x.data(), std::min(x.size(), size_t(2)));
    pos = pos + 8;
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinLimited::encode<native>(void* data) const;
template size_t BuiltinLimited::encode<little>(void* data) const;
template size_t BuiltinLimited::encode<big>(void* data) const;

template <endianness E>
size_t BuiltinGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinGreedy::encode<native>(void* data) const;
template size_t BuiltinGreedy::encode<little>(void* data) const;
template size_t BuiltinGreedy::encode<big>(void* data) const;

template <endianness E>
size_t Fixcomp::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Fixcomp::encode<native>(void* data) const;
template size_t Fixcomp::encode<little>(void* data) const;
template size_t Fixcomp::encode<big>(void* data) const;

template <endianness E>
size_t FixcompFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x, 2);
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompFixed::encode<native>(void* data) const;
template size_t FixcompFixed::encode<little>(void* data) const;
template size_t FixcompFixed::encode<big>(void* data) const;

template <endianness E>
size_t FixcompDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompDynamic::encode<native>(void* data) const;
template size_t FixcompDynamic::encode<little>(void* data) const;
template size_t FixcompDynamic::encode<big>(void* data) const;

template <endianness E>
size_t FixcompLimited::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(std::min(x.size(), size_t(2))));
    do_encode<E>(pos, x.data(), std::min(x.size(), size_t(2)));
    pos = pos + 16;
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompLimited::encode<native>(void* data) const;
template size_t FixcompLimited::encode<little>(void* data) const;
template size_t FixcompLimited::encode<big>(void* data) const;

template <endianness E>
size_t FixcompGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompGreedy::encode<native>(void* data) const;
template size_t FixcompGreedy::encode<little>(void* data) const;
template size_t FixcompGreedy::encode<big>(void* data) const;

template <endianness E>
size_t Dyncomp::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Dyncomp::encode<native>(void* data) const;
template size_t Dyncomp::encode<little>(void* data) const;
template size_t Dyncomp::encode<big>(void* data) const;

template <endianness E>
size_t DyncompDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t DyncompDynamic::encode<native>(void* data) const;
template size_t DyncompDynamic::encode<little>(void* data) const;
template size_t DyncompDynamic::encode<big>(void* data) const;

template <endianness E>
size_t DyncompGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t DyncompGreedy::encode<native>(void* data) const;
template size_t DyncompGreedy::encode<little>(void* data) const;
template size_t DyncompGreedy::encode<big>(void* data) const;
