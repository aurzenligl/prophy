#ifndef _PROPHY_GENERATED_Arrays_HPP
#define _PROPHY_GENERATED_Arrays_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/endianness.hpp>
#include <prophy/detail/byte_size.hpp>

struct Builtin
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint32_t y;

    Builtin(): x(), y() { }

    size_t get_byte_size() const
    {
        return 8;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BuiltinFixed
{
    enum { encoded_byte_size = 8 };

    uint32_t x[2];

    BuiltinFixed(): x() { }

    size_t get_byte_size() const
    {
        return 8;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BuiltinDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x;

    size_t get_byte_size() const
    {
        return 4 + x.size() * 4;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BuiltinLimited
{
    enum { encoded_byte_size = 12 };

    std::vector<uint32_t> x; /// limit 2

    size_t get_byte_size() const
    {
        return 12;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct BuiltinGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x; /// greedy

    size_t get_byte_size() const
    {
        return x.size() * 4;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct Fixcomp
{
    enum { encoded_byte_size = 16 };

    Builtin x;
    Builtin y;

    size_t get_byte_size() const
    {
        return 16;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct FixcompFixed
{
    enum { encoded_byte_size = 16 };

    Builtin x[2];

    size_t get_byte_size() const
    {
        return 16;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct FixcompDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<Builtin> x;

    size_t get_byte_size() const
    {
        return 4 + x.size() * 8;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct FixcompLimited
{
    enum { encoded_byte_size = 20 };

    std::vector<Builtin> x; /// limit 2

    size_t get_byte_size() const
    {
        return 20;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct FixcompGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<Builtin> x; /// greedy

    size_t get_byte_size() const
    {
        return x.size() * 8;
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct Dyncomp
{
    enum { encoded_byte_size = -1 };

    BuiltinDynamic x;

    size_t get_byte_size() const
    {
        return x.get_byte_size();
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DyncompDynamic
{
    enum { encoded_byte_size = -1 };

    std::vector<BuiltinDynamic> x;

    size_t get_byte_size() const
    {
        return 4 + std::accumulate(x.begin(), x.end(), size_t(), prophy::detail::byte_size());
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

struct DyncompGreedy
{
    enum { encoded_byte_size = -1 };

    std::vector<BuiltinDynamic> x; /// greedy

    size_t get_byte_size() const
    {
        return std::accumulate(x.begin(), x.end(), size_t(), prophy::detail::byte_size());
    }

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const
    {
        return encode<prophy::native>(data);
    }
};

#endif  /* _PROPHY_GENERATED_Arrays_HPP */
