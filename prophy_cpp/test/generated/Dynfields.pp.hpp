#ifndef _PROPHY_GENERATED_Dynfields_HPP
#define _PROPHY_GENERATED_Dynfields_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>

struct Dynfields
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    std::vector<uint16_t> y;
    uint64_t z;

    Dynfields(): z() { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<8>(
            prophy::detail::nearest<2>(
               4 + x.size()
            ) + 2 + 2 * y.size()
        ) + 8;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DynfieldsMixed
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    std::vector<uint16_t> y;

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            prophy::detail::nearest<2>(
                6 + x.size()
            ) + 2 * y.size()
        );
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DynfieldsOverlapped
{
    enum { encoded_byte_size = -1 };

    std::vector<uint16_t> b;
    std::vector<uint16_t> c;
    std::vector<uint16_t> a;

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            prophy::detail::nearest<4>(
                8 + 2 * b.size()
            ) + 4 + 2 * c.size() + 2 * a.size()
        );
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DynfieldsPartialpad_Helper
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    uint8_t y;
    uint64_t z;

    DynfieldsPartialpad_Helper(): y(), z() { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<8>(
            1 + x.size()
        ) + 16;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DynfieldsPartialpad
{
    enum { encoded_byte_size = -1 };

    uint8_t x;
    DynfieldsPartialpad_Helper y;

    DynfieldsPartialpad(): x() { }

    size_t get_byte_size() const
    {
        return 8 + y.get_byte_size();
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DynfieldsScalarpartialpad_Helper
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size()
        );
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DynfieldsScalarpartialpad
{
    enum { encoded_byte_size = -1 };

    DynfieldsScalarpartialpad_Helper x;
    DynfieldsScalarpartialpad_Helper y;
    DynfieldsScalarpartialpad_Helper z;

    size_t get_byte_size() const
    {
        return x.get_byte_size() + y.get_byte_size() + z.get_byte_size();
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

#endif  /* _PROPHY_GENERATED_Dynfields_HPP */
