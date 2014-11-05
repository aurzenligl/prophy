#ifndef _PROPHY_GENERATED_FULL_Dynfields_HPP
#define _PROPHY_GENERATED_FULL_Dynfields_HPP

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

struct Dynfields : public prophy::detail::message<Dynfields>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    std::vector<uint16_t> y;
    uint64_t z;

    Dynfields(): z() { }
    Dynfields(const std::vector<uint8_t>& _1, const std::vector<uint16_t>& _2, uint64_t _3): x(_1), y(_2), z(_3) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<8>(
            prophy::detail::nearest<2>(
               4 + x.size()
            ) + 2 + 2 * y.size()
        ) + 8;
    }
};

struct DynfieldsMixed : public prophy::detail::message<DynfieldsMixed>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    std::vector<uint16_t> y;

    DynfieldsMixed() { }
    DynfieldsMixed(const std::vector<uint8_t>& _1, const std::vector<uint16_t>& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            prophy::detail::nearest<2>(
                6 + x.size()
            ) + 2 * y.size()
        );
    }
};

struct DynfieldsOverlapped : public prophy::detail::message<DynfieldsOverlapped>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint16_t> b;
    std::vector<uint16_t> c;
    std::vector<uint16_t> a;

    DynfieldsOverlapped() { }
    DynfieldsOverlapped(const std::vector<uint16_t>& _1, const std::vector<uint16_t>& _2, const std::vector<uint16_t>& _3): b(_1), c(_2), a(_3) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            prophy::detail::nearest<4>(
                8 + 2 * b.size()
            ) + 4 + 2 * c.size() + 2 * a.size()
        );
    }
};

struct DynfieldsPartialpad_Helper : public prophy::detail::message<DynfieldsPartialpad_Helper>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;
    uint8_t y;
    uint64_t z;

    DynfieldsPartialpad_Helper(): y(), z() { }
    DynfieldsPartialpad_Helper(const std::vector<uint8_t>& _1, uint8_t _2, uint64_t _3): x(_1), y(_2), z(_3) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<8>(
            1 + x.size()
        ) + 16;
    }
};

struct DynfieldsPartialpad : public prophy::detail::message<DynfieldsPartialpad>
{
    enum { encoded_byte_size = -1 };

    uint8_t x;
    DynfieldsPartialpad_Helper y;

    DynfieldsPartialpad(): x() { }
    DynfieldsPartialpad(uint8_t _1, const DynfieldsPartialpad_Helper& _2): x(_1), y(_2) { }

    size_t get_byte_size() const
    {
        return 8 + y.get_byte_size();
    }
};

struct DynfieldsScalarpartialpad_Helper : public prophy::detail::message<DynfieldsScalarpartialpad_Helper>
{
    enum { encoded_byte_size = -1 };

    std::vector<uint8_t> x;

    DynfieldsScalarpartialpad_Helper() { }
    DynfieldsScalarpartialpad_Helper(const std::vector<uint8_t>& _1): x(_1) { }

    size_t get_byte_size() const
    {
        return prophy::detail::nearest<4>(
            4 + x.size()
        );
    }
};

struct DynfieldsScalarpartialpad : public prophy::detail::message<DynfieldsScalarpartialpad>
{
    enum { encoded_byte_size = -1 };

    DynfieldsScalarpartialpad_Helper x;
    DynfieldsScalarpartialpad_Helper y;
    DynfieldsScalarpartialpad_Helper z;

    DynfieldsScalarpartialpad() { }
    DynfieldsScalarpartialpad(const DynfieldsScalarpartialpad_Helper& _1, const DynfieldsScalarpartialpad_Helper& _2, const DynfieldsScalarpartialpad_Helper& _3): x(_1), y(_2), z(_3) { }

    size_t get_byte_size() const
    {
        return x.get_byte_size() + y.get_byte_size() + z.get_byte_size();
    }
};

} // namespace generated
} // namespace prophy

#endif  /* _PROPHY_GENERATED_FULL_Dynfields_HPP */
