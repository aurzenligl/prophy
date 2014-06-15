#include <gtest/gtest.h>

#include <prophy/prophy.hpp>

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
