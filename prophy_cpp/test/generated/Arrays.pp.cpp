#include "Arrays.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
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

template <endianness E>
size_t BuiltinFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x, 2);
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinFixed::encode<native>(void* data) const;

template <endianness E>
size_t BuiltinDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinDynamic::encode<native>(void* data) const;

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

template <endianness E>
size_t BuiltinGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t BuiltinGreedy::encode<native>(void* data) const;

template <endianness E>
size_t Fixcomp::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Fixcomp::encode<native>(void* data) const;

template <endianness E>
size_t FixcompFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x, 2);
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompFixed::encode<native>(void* data) const;

template <endianness E>
size_t FixcompDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompDynamic::encode<native>(void* data) const;

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

template <endianness E>
size_t FixcompGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t FixcompGreedy::encode<native>(void* data) const;

template <endianness E>
size_t Dyncomp::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Dyncomp::encode<native>(void* data) const;

template <endianness E>
size_t DyncompDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    return pos - static_cast<uint8_t*>(data);
}

template size_t DyncompDynamic::encode<native>(void* data) const;
