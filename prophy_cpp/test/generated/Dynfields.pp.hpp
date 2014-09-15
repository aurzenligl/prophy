#ifndef _PROPHY_GENERATED_Dynfields_HPP
#define _PROPHY_GENERATED_Dynfields_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/endianness.hpp>

struct Dynfields
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    std::vector<uint16_t> y;
    uint64_t z;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct DynfieldsMixed
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    std::vector<uint16_t> y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct DynfieldsOverlapped
{
    enum { encoded_byte_size = -1 };

    std::vector<uint16_t> b;
    std::vector<uint16_t> c;
    std::vector<uint16_t> a;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct DynfieldsPartialpad_Helper
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    uint8_t y;
    uint64_t z;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct DynfieldsPartialpad
{
    enum { encoded_byte_size = -1 };

    uint8_t x;
    DynfieldsPartialpad_Helper y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct DynfieldsScalarpartialpad_Helper
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct DynfieldsScalarpartialpad
{
    enum { encoded_byte_size = -1 };

    DynfieldsScalarpartialpad_Helper x;
    DynfieldsScalarpartialpad_Helper y;
    DynfieldsScalarpartialpad_Helper z;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Dynfields_HPP */
