#include "Paddings.pp.hpp"
#include <algorithm>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/align.hpp>

using namespace prophy;
using namespace prophy::detail;

template <endianness E>
size_t Endpad::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y);
    pos = pos + 1;
    return pos - static_cast<uint8_t*>(data);
}

template size_t Endpad::encode<native>(void* data) const;

template <endianness E>
size_t EndpadFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y, 3);
    pos = pos + 1;
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadFixed::encode<native>(void* data) const;

template <endianness E>
size_t EndpadDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    pos = align<4>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadDynamic::encode<native>(void* data) const;

template <endianness E>
size_t EndpadLimited::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(std::min(x.size(), size_t(2))));
    do_encode<E>(pos, x.data(), std::min(x.size(), size_t(2)));
    pos = pos + 4;
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadLimited::encode<native>(void* data) const;

template <endianness E>
size_t EndpadGreedy::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x));
    pos = do_encode<E>(pos, y.data(), y.size());
    pos = align<4>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t EndpadGreedy::encode<native>(void* data) const;

template <endianness E>
size_t Scalarpad::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = pos + 1;
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t Scalarpad::encode<native>(void* data) const;

template <endianness E>
size_t ScalarpadComppre_Helper::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ScalarpadComppre_Helper::encode<native>(void* data) const;

template <endianness E>
size_t ScalarpadComppre::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = pos + 1;
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ScalarpadComppre::encode<native>(void* data) const;

template <endianness E>
size_t ScalarpadComppost_Helper::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ScalarpadComppost_Helper::encode<native>(void* data) const;

template <endianness E>
size_t ScalarpadComppost::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = pos + 1;
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ScalarpadComppost::encode<native>(void* data) const;

template <endianness E>
size_t UnionpadOptionalboolpad::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = pos + 3;
    pos = do_encode<E>(pos, uint32_t(has_y));
    pos = do_encode<E>(pos, y);
    pos = pos + 3;
    return pos - static_cast<uint8_t*>(data);
}

template size_t UnionpadOptionalboolpad::encode<native>(void* data) const;

template <endianness E>
size_t UnionpadOptionalvaluepad::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(has_x));
    pos = pos + 4;
    pos = do_encode<E>(pos, x);
    return pos - static_cast<uint8_t*>(data);
}

template size_t UnionpadOptionalvaluepad::encode<native>(void* data) const;

template <endianness E>
size_t UnionpadDiscpad_Helper::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(discriminator));
    switch(discriminator)
    {
        case discriminator_a:
            do_encode<E>(pos, a);
            break;
    }
    pos = pos + 4;
    return pos - static_cast<uint8_t*>(data);
}

template size_t UnionpadDiscpad_Helper::encode<native>(void* data) const;

template <endianness E>
size_t UnionpadDiscpad::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = pos + 3;
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t UnionpadDiscpad::encode<native>(void* data) const;

template <endianness E>
size_t UnionpadArmpad_Helper::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(discriminator));
    pos = pos + 4;
    switch(discriminator)
    {
        case discriminator_a:
            do_encode<E>(pos, a);
            break;
        case discriminator_b:
            do_encode<E>(pos, b);
            break;
    }
    pos = pos + 8;
    return pos - static_cast<uint8_t*>(data);
}

template size_t UnionpadArmpad_Helper::encode<native>(void* data) const;

template <endianness E>
size_t UnionpadArmpad::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = pos + 7;
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t UnionpadArmpad::encode<native>(void* data) const;

template <endianness E>
size_t ArraypadCounter::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint8_t(x.size()));
    pos = pos + 1;
    pos = do_encode<E>(pos, x.data(), uint8_t(x.size()));
    return pos - static_cast<uint8_t*>(data);
}

template size_t ArraypadCounter::encode<native>(void* data) const;

template <endianness E>
size_t ArraypadCounterSeparated::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint8_t(x.size()));
    pos = pos + 3;
    pos = do_encode<E>(pos, y);
    pos = do_encode<E>(pos, x.data(), uint8_t(x.size()));
    return pos - static_cast<uint8_t*>(data);
}

template size_t ArraypadCounterSeparated::encode<native>(void* data) const;

template <endianness E>
size_t ArraypadCounterAligns_Helper::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint16_t(x.size()));
    pos = do_encode<E>(pos, x.data(), uint16_t(x.size()));
    pos = align<2>(pos);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ArraypadCounterAligns_Helper::encode<native>(void* data) const;

template <endianness E>
size_t ArraypadCounterAligns::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = pos + 1;
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ArraypadCounterAligns::encode<native>(void* data) const;

template <endianness E>
size_t ArraypadFixed::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, x);
    pos = do_encode<E>(pos, y, 3);
    pos = pos + 1;
    pos = do_encode<E>(pos, z);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ArraypadFixed::encode<native>(void* data) const;

template <endianness E>
size_t ArraypadDynamic::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(x.size()));
    pos = do_encode<E>(pos, x.data(), x.size());
    pos = align<4>(pos);
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ArraypadDynamic::encode<native>(void* data) const;

template <endianness E>
size_t ArraypadLimited::encode(void* data) const
{
    uint8_t* pos = static_cast<uint8_t*>(data);
    pos = do_encode<E>(pos, uint32_t(std::min(x.size(), size_t(2))));
    do_encode<E>(pos, x.data(), std::min(x.size(), size_t(2)));
    pos = pos + 2;
    pos = pos + 2;
    pos = do_encode<E>(pos, y);
    return pos - static_cast<uint8_t*>(data);
}

template size_t ArraypadLimited::encode<native>(void* data) const;
