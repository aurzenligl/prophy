#include <string>
#include <gtest/gtest.h>
#include <prophy/detail/encoder.hpp>
#include <prophy/detail/decoder.hpp>
#include "util.hpp"

using namespace testing;
using namespace prophy;
using namespace prophy::detail;

/// * WARNING * This test group assumes you're running on little endian machine.

TEST(encoding_ints, int8)
{
    uint8_t data;
    int8_t& idata = *reinterpret_cast<int8_t*>(&data);
    uint8_t* bdata = reinterpret_cast<uint8_t*>(&data);

    encode_int<native, int8_t>(bdata, 0x01);
    EXPECT_EQ(bytes("\x01"), bytes(&data, 1));

    encode_int<native, uint8_t>(bdata, 0x01);
    EXPECT_EQ(bytes("\x01"), bytes(&data, 1));

    encode_int<little, int8_t>(bdata, 0x01);
    EXPECT_EQ(bytes("\x01"), bytes(&data, 1));

    encode_int<little, uint8_t>(bdata, 0x01);
    EXPECT_EQ(bytes("\x01"), bytes(&data, 1));

    encode_int<big, int8_t>(bdata, 0x01);
    EXPECT_EQ(bytes("\x01"), bytes(&data, 1));

    encode_int<big, uint8_t>(bdata, 0x01);
    EXPECT_EQ(bytes("\x01"), bytes(&data, 1));

    decode_int<native, int8_t>(idata, reinterpret_cast<const uint8_t*>("\x01"));
    EXPECT_EQ(1, data);

    decode_int<native, uint8_t>(data, reinterpret_cast<const uint8_t*>("\x01"));
    EXPECT_EQ(1, data);

    decode_int<little, int8_t>(idata, reinterpret_cast<const uint8_t*>("\x01"));
    EXPECT_EQ(1, data);

    decode_int<little, uint8_t>(data, reinterpret_cast<const uint8_t*>("\x01"));
    EXPECT_EQ(1, data);

    decode_int<big, int8_t>(idata, reinterpret_cast<const uint8_t*>("\x01"));
    EXPECT_EQ(1, data);

    decode_int<big, uint8_t>(data, reinterpret_cast<const uint8_t*>("\x01"));
    EXPECT_EQ(1, data);
}

TEST(encoding_ints, int16)
{
    uint16_t data;
    int16_t& idata = *reinterpret_cast<int16_t*>(&data);
    uint8_t* bdata = reinterpret_cast<uint8_t*>(&data);

    encode_int<native, int16_t>(bdata, 0x0102);
    EXPECT_EQ(bytes("\x02\x01"), bytes(&data, 2));

    encode_int<native, uint16_t>(bdata, 0x0102);
    EXPECT_EQ(bytes("\x02\x01"), bytes(&data, 2));

    encode_int<little, int16_t>(bdata, 0x0102);
    EXPECT_EQ(bytes("\x02\x01"), bytes(&data, 2));

    encode_int<little, uint16_t>(bdata, 0x0102);
    EXPECT_EQ(bytes("\x02\x01"), bytes(&data, 2));

    encode_int<big, int16_t>(bdata, 0x0102);
    EXPECT_EQ(bytes("\x01\x02"), bytes(&data, 2));

    encode_int<big, uint16_t>(bdata, 0x0102);
    EXPECT_EQ(bytes("\x01\x02"), bytes(&data, 2));

    decode_int<native, int16_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02"));
    EXPECT_EQ(0x0201, data);

    decode_int<native, uint16_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02"));
    EXPECT_EQ(0x0201, data);

    decode_int<little, int16_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02"));
    EXPECT_EQ(0x0201, data);

    decode_int<little, uint16_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02"));
    EXPECT_EQ(0x0201, data);

    decode_int<big, int16_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02"));
    EXPECT_EQ(0x0102, data);

    decode_int<big, uint16_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02"));
    EXPECT_EQ(0x0102, data);
}

TEST(encoding_ints, int32)
{
    uint32_t data;
    int32_t& idata = *reinterpret_cast<int32_t*>(&data);
    uint8_t* bdata = reinterpret_cast<uint8_t*>(&data);

    encode_int<native, int32_t>(bdata, 0x01020304);
    EXPECT_EQ(bytes("\x04\x03\x02\x01"), bytes(&data, 4));

    encode_int<native, uint32_t>(bdata, 0x01020304);
    EXPECT_EQ(bytes("\x04\x03\x02\x01"), bytes(&data, 4));

    encode_int<little, int32_t>(bdata, 0x01020304);
    EXPECT_EQ(bytes("\x04\x03\x02\x01"), bytes(&data, 4));

    encode_int<little, uint32_t>(bdata, 0x01020304);
    EXPECT_EQ(bytes("\x04\x03\x02\x01"), bytes(&data, 4));

    encode_int<big, int32_t>(bdata, 0x01020304);
    EXPECT_EQ(bytes("\x01\x02\x03\x04"), bytes(&data, 4));

    encode_int<big, uint32_t>(bdata, 0x01020304);
    EXPECT_EQ(bytes("\x01\x02\x03\x04"), bytes(&data, 4));

    decode_int<native, int32_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04"));
    EXPECT_EQ(0x04030201, data);

    decode_int<native, uint32_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04"));
    EXPECT_EQ(0x04030201, data);

    decode_int<little, int32_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04"));
    EXPECT_EQ(0x04030201, data);

    decode_int<little, uint32_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04"));
    EXPECT_EQ(0x04030201, data);

    decode_int<big, int32_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04"));
    EXPECT_EQ(0x01020304, data);

    decode_int<big, uint32_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04"));
    EXPECT_EQ(0x01020304, data);
}

TEST(encoding_ints, int64)
{
    uint64_t data;
    int64_t& idata = *reinterpret_cast<int64_t*>(&data);
    uint8_t* bdata = reinterpret_cast<uint8_t*>(&data);

    encode_int<native, int64_t>(bdata, 0x0102030405060708ULL);
    EXPECT_EQ(bytes("\x08\x07\x06\x05\x04\x03\x02\x01"), bytes(&data, 8));

    encode_int<native, uint64_t>(bdata, 0x0102030405060708ULL);
    EXPECT_EQ(bytes("\x08\x07\x06\x05\x04\x03\x02\x01"), bytes(&data, 8));

    encode_int<little, int64_t>(bdata, 0x0102030405060708ULL);
    EXPECT_EQ(bytes("\x08\x07\x06\x05\x04\x03\x02\x01"), bytes(&data, 8));

    encode_int<little, uint64_t>(bdata, 0x0102030405060708ULL);
    EXPECT_EQ(bytes("\x08\x07\x06\x05\x04\x03\x02\x01"), bytes(&data, 8));

    encode_int<big, int64_t>(bdata, 0x0102030405060708ULL);
    EXPECT_EQ(bytes("\x01\x02\x03\x04\x05\x06\x07\x08"), bytes(&data, 8));

    encode_int<big, uint64_t>(bdata, 0x0102030405060708ULL);
    EXPECT_EQ(bytes("\x01\x02\x03\x04\x05\x06\x07\x08"), bytes(&data, 8));

    decode_int<native, int64_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04\x05\x06\x07\x08"));
    EXPECT_EQ(0x0807060504030201ULL, data);

    decode_int<native, uint64_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04\x05\x06\x07\x08"));
    EXPECT_EQ(0x0807060504030201ULL, data);

    decode_int<little, int64_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04\x05\x06\x07\x08"));
    EXPECT_EQ(0x0807060504030201ULL, data);

    decode_int<little, uint64_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04\x05\x06\x07\x08"));
    EXPECT_EQ(0x0807060504030201ULL, data);

    decode_int<big, int64_t>(idata, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04\x05\x06\x07\x08"));
    EXPECT_EQ(0x0102030405060708ULL, data);

    decode_int<big, uint64_t>(data, reinterpret_cast<const uint8_t*>("\x01\x02\x03\x04\x05\x06\x07\x08"));
    EXPECT_EQ(0x0102030405060708ULL, data);
}

TEST(encoding_ints, floats)
{
    float data;
    uint8_t* bdata = reinterpret_cast<uint8_t*>(&data);

    encode_int<native, float>(bdata, 10);
    EXPECT_EQ(bytes("\x00\x00\x20\x41"), bytes(&data, 4));

    encode_int<little, float>(bdata, 10);
    EXPECT_EQ(bytes("\x00\x00\x20\x41"), bytes(&data, 4));

    encode_int<big, float>(bdata, 10);
    EXPECT_EQ(bytes("\x41\x20\x00\x00"), bytes(&data, 4));

    decode_int<native, float>(data, reinterpret_cast<const uint8_t*>("\x00\x00\x20\x41"));
    EXPECT_EQ(10, data);

    decode_int<little, float>(data, reinterpret_cast<const uint8_t*>("\x00\x00\x20\x41"));
    EXPECT_EQ(10, data);

    decode_int<big, float>(data, reinterpret_cast<const uint8_t*>("\x41\x20\x00\x00"));
    EXPECT_EQ(10, data);
}

TEST(encoding_ints, doubles)
{
    double data;
    uint8_t* bdata = reinterpret_cast<uint8_t*>(&data);

    encode_int<native, double>(bdata, 10);
    EXPECT_EQ(bytes("\x00\x00\x00\x00\x00\x00\x24\x40"), bytes(&data, 8));

    encode_int<little, double>(bdata, 10);
    EXPECT_EQ(bytes("\x00\x00\x00\x00\x00\x00\x24\x40"), bytes(&data, 8));

    encode_int<big, double>(bdata, 10);
    EXPECT_EQ(bytes("\x40\x24\x00\x00\x00\x00\x00\x00"), bytes(&data, 8));

    decode_int<native, double>(data, reinterpret_cast<const uint8_t*>("\x00\x00\x00\x00\x00\x00\x24\x40"));
    EXPECT_EQ(10, data);

    decode_int<little, double>(data, reinterpret_cast<const uint8_t*>("\x00\x00\x00\x00\x00\x00\x24\x40"));
    EXPECT_EQ(10, data);

    decode_int<big, double>(data, reinterpret_cast<const uint8_t*>("\x40\x24\x00\x00\x00\x00\x00\x00"));
    EXPECT_EQ(10, data);
}
