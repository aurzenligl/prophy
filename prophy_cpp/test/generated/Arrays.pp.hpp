#ifndef _PROPHY_GENERATED_Array_HPP
#define _PROPHY_GENERATED_Array_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/endianness.hpp>

struct Builtin
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint32_t y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinFixed
{
    enum { encoded_byte_size = 8 };

    uint32_t x[2];

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinLimited
{
    enum { encoded_byte_size = 12 };

    std::vector<uint32_t> x; /// limit 2

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct BuiltinGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x; /// greedy

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct Fixcomp
{
    enum { encoded_byte_size = 16 };

    Builtin x;
    Builtin y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct FixcompFixed
{
    enum { encoded_byte_size = 16 };

    Builtin x[2];

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct FixcompDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<Builtin> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct FixcompLimited
{
    enum { encoded_byte_size = 20 };

    std::vector<Builtin> x; /// limit 2

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct FixcompGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<Builtin> x; /// greedy

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct Dyncomp
{
    enum { encoded_byte_size = -1 };

    BuiltinDynamic x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

struct DyncompDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<BuiltinDynamic> x;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

#endif  /* _PROPHY_GENERATED_Array_HPP */
