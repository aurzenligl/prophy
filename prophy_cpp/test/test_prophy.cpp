#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include <prophy/prophy.hpp>

#include "util.hpp"

TEST(prophy, swaps_u8)
{
    uint8_t x = 0x01;
    prophy::swap(x);
    EXPECT_EQ(0x01, x);
}

TEST(prophy, swaps_u16)
{
    uint16_t x = 0x0102;
    prophy::swap(x);
    EXPECT_EQ(0x0201, x);
}

TEST(prophy, swaps_u32)
{
    uint32_t x = 0x01020304;
    prophy::swap(x);
    EXPECT_EQ(0x04030201, x);
}

TEST(prophy, swaps_u64)
{
    uint64_t x = 0x0102030405060708ULL;
    prophy::swap(x);
    EXPECT_EQ(0x0807060504030201ULL, x);
}

TEST(prophy, swaps_i8)
{
    int8_t x = 0x80;
    prophy::swap(x);
    EXPECT_EQ(int8_t(0x80), x);
}

TEST(prophy, swaps_i16)
{
    int16_t x = 0x8070;
    prophy::swap(x);
    EXPECT_EQ(int16_t(0x7080), x);
}

TEST(prophy, swaps_i32)
{
    int32_t x = 0x80706050;
    prophy::swap(x);
    EXPECT_EQ(int32_t(0x50607080), x);
}

TEST(prophy, swaps_i64)
{
    int64_t x = 0x8070605040302010ULL;
    prophy::swap(x);
    EXPECT_EQ(int64_t(0x1020304050607080ULL), x);
}

TEST(prophy, swaps_float)
{
    union
    {
        float x;
        uint32_t data;
    } x;
    x.data = 0x01020304;
    prophy::swap(x.x);
    EXPECT_EQ(0x04030201, x.data);
}

TEST(prophy, swaps_double)
{
    union
    {
        double x;
        uint64_t data;
    } x;
    x.data = 0x0102030405060708ULL;
    prophy::swap(x.x);
    EXPECT_EQ(0x0807060504030201ULL, x.data);
}

struct X
{
    uint32_t x;
    uint64_t y;
};

struct Y
{
    uint16_t x[2];
    uint8_t y;
};

TEST(prophy, calculates_alignment)
{
    EXPECT_EQ(8, prophy::alignment<X>::value);
    EXPECT_EQ(2, prophy::alignment<Y>::value);
}

TEST(prophy, aligns_pointers)
{
    EXPECT_EQ(0, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<X*>(uintptr_t(0)))));
    EXPECT_EQ(8, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<X*>(uintptr_t(1)))));
    EXPECT_EQ(8, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<X*>(uintptr_t(3)))));
    EXPECT_EQ(8, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<X*>(uintptr_t(7)))));
    EXPECT_EQ(16, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<X*>(uintptr_t(9)))));

    EXPECT_EQ(0, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<Y*>(uintptr_t(0)))));
    EXPECT_EQ(2, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<Y*>(uintptr_t(1)))));
    EXPECT_EQ(2, reinterpret_cast<uintptr_t>(prophy::align(reinterpret_cast<Y*>(uintptr_t(2)))));
}

TEST(prophy, casts_pointers_ensuring_alignment)
{
    EXPECT_EQ(8, reinterpret_cast<uintptr_t>(prophy::cast<X*>(reinterpret_cast<uint16_t*>(uintptr_t(2)))));

    EXPECT_EQ(2, reinterpret_cast<uintptr_t>(prophy::cast<Y*>(reinterpret_cast<uint8_t*>(uintptr_t(1)))));
}

struct DynamicFixedArray
{
    uint8_t num_of_x;
    uint16_t x[1];
};

inline DynamicFixedArray* swap(DynamicFixedArray& in)
{
    prophy::swap(in.num_of_x);
    return prophy::cast<DynamicFixedArray*>(prophy::swap_n_fixed(in.x, in.num_of_x));
}

TEST(prophy, swaps_fixed_array)
{
    std::vector<uint8_t> input = to_vector(
        "\x05\x00"
        "\x00\x01"
        "\x00\x02"
        "\x00\x03"
        "\x00\x04"
        "\x00\x05"
    );
    std::vector<uint8_t> output = to_vector(
        "\x05\x00"
        "\x01\x00"
        "\x02\x00"
        "\x03\x00"
        "\x04\x00"
        "\x05\x00"
    );

    DynamicFixedArray* x = reinterpret_cast<DynamicFixedArray*>(input.data());

    swap(*x);

    EXPECT_THAT(input, ::testing::ContainerEq(output));
}

struct DynamicDynamicArray
{
    uint8_t num_of_x;
    DynamicFixedArray x[1];
};

inline DynamicDynamicArray* swap(DynamicDynamicArray& in)
{
    prophy::swap(in.num_of_x);
    return prophy::cast<DynamicDynamicArray*>(prophy::swap_n_dynamic(in.x, in.num_of_x));
}

TEST(prophy, swaps_dynamic_array)
{
    std::vector<uint8_t> input = to_vector(
        "\x03\x00"

        "\x01\x00"
        "\x00\x01"

        "\x05\x00"
        "\x00\x02"
        "\x00\x03"
        "\x00\x04"
        "\x00\x05"
        "\x00\x06"

        "\x03\x00"
        "\x00\x07"
        "\x00\x08"
        "\x00\x09"
    );
    std::vector<uint8_t> output = to_vector(
        "\x03\x00"

        "\x01\x00"
        "\x01\x00"

        "\x05\x00"
        "\x02\x00"
        "\x03\x00"
        "\x04\x00"
        "\x05\x00"
        "\x06\x00"

        "\x03\x00"
        "\x07\x00"
        "\x08\x00"
        "\x09\x00"
    );

    DynamicDynamicArray* x = reinterpret_cast<DynamicDynamicArray*>(input.data());

    swap(*x);

    EXPECT_THAT(input, ::testing::ContainerEq(output));
}
