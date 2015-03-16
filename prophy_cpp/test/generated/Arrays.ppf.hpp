#ifndef _PROPHY_GENERATED_FULL_Arrays_HPP
#define _PROPHY_GENERATED_FULL_Arrays_HPP

#include <stdint.h>
#include <numeric>
#include <vector>
#include <string>
#include <prophy/array.hpp>
#include <prophy/endianness.hpp>
#include <prophy/optional.hpp>
#include <prophy/detail/byte_size.hpp>
#include <prophy/detail/message.hpp>
#include <prophy/detail/mpl.hpp>

namespace prophy
{
namespace generated
{

struct Builtin : public prophy::detail::message<Builtin>
{
    enum { encoded_byte_size = 8 };

    uint32_t x;
    uint32_t y;

    Builtin(): x(), y() { }
    Builtin(uint32_t _1, uint32_t _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct BuiltinFixed : public prophy::detail::message<BuiltinFixed>
{
    enum { encoded_byte_size = 8 };

    array<uint32_t, 2> x;

    BuiltinFixed(): x() { }
    BuiltinFixed(const array<uint32_t, 2>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 8;
    }
};

struct BuiltinDynamic : public prophy::detail::message<BuiltinDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x;

    BuiltinDynamic() { }
    BuiltinDynamic(const std::vector<uint32_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 4 + x.size() * 4;
    }
};

struct BuiltinLimited : public prophy::detail::message<BuiltinLimited>
{
    enum { encoded_byte_size = 12 };

    std::vector<uint32_t> x; /// limit 2

    BuiltinLimited() { }
    BuiltinLimited(const std::vector<uint32_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 12;
    }
};

struct BuiltinGreedy : public prophy::detail::message<BuiltinGreedy>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint32_t> x; /// greedy

    BuiltinGreedy() { }
    BuiltinGreedy(const std::vector<uint32_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return x.size() * 4;
    }
};

struct Fixcomp : public prophy::detail::message<Fixcomp>
{
    enum { encoded_byte_size = 16 };

    Builtin x;
    Builtin y;

    Fixcomp() { }
    Fixcomp(const Builtin& _1, const Builtin& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct FixcompFixed : public prophy::detail::message<FixcompFixed>
{
    enum { encoded_byte_size = 16 };

    array<Builtin, 2> x;

    FixcompFixed(): x() { }
    FixcompFixed(const array<Builtin, 2>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 16;
    }
};

struct FixcompDynamic : public prophy::detail::message<FixcompDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<Builtin> x;

    FixcompDynamic() { }
    FixcompDynamic(const std::vector<Builtin>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 4 + x.size() * 8;
    }
};

struct FixcompLimited : public prophy::detail::message<FixcompLimited>
{
    enum { encoded_byte_size = 20 };

    std::vector<Builtin> x; /// limit 2

    FixcompLimited() { }
    FixcompLimited(const std::vector<Builtin>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 20;
    }
};

struct FixcompGreedy : public prophy::detail::message<FixcompGreedy>
{
    enum { encoded_byte_size = -1 };

    std::vector<Builtin> x; /// greedy

    FixcompGreedy() { }
    FixcompGreedy(const std::vector<Builtin>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return x.size() * 8;
    }
};

struct Dyncomp : public prophy::detail::message<Dyncomp>
{
    enum { encoded_byte_size = -1 };

    BuiltinDynamic x;

    Dyncomp() { }
    Dyncomp(const BuiltinDynamic& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return x.get_byte_size();
    }
};

struct DyncompDynamic : public prophy::detail::message<DyncompDynamic>
{
    enum { encoded_byte_size = -1 };

    std::vector<BuiltinDynamic> x;

    DyncompDynamic() { }
    DyncompDynamic(const std::vector<BuiltinDynamic>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return 4 + std::accumulate(x.begin(), x.end(), size_t(), prophy::detail::byte_size());
    }
};

struct DyncompGreedy : public prophy::detail::message<DyncompGreedy>
{
    enum { encoded_byte_size = -1 };

    std::vector<BuiltinDynamic> x; /// greedy

    DyncompGreedy() { }
    DyncompGreedy(const std::vector<BuiltinDynamic>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return std::accumulate(x.begin(), x.end(), size_t(), prophy::detail::byte_size());
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_Arrays_HPP */
