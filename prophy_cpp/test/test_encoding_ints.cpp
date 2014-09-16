#include <string>
#include <gtest/gtest.h>
#include <prophy/detail/encoder.hpp>

using namespace testing;
using namespace prophy;
using namespace prophy::detail;

/// * WARNING * This test group assumes you're running on little endian machine.

TEST(encoding_ints, int8)
{
    uint8_t data;

    encode_int<native, int8_t>(reinterpret_cast<uint8_t*>(&data), 0x01);
    EXPECT_EQ(std::string("\x01", 1), std::string(reinterpret_cast<char*>(&data), 1));

    encode_int<native, uint8_t>(reinterpret_cast<uint8_t*>(&data), 0x01);
    EXPECT_EQ(std::string("\x01", 1), std::string(reinterpret_cast<char*>(&data), 1));

    encode_int<little, int8_t>(reinterpret_cast<uint8_t*>(&data), 0x01);
    EXPECT_EQ(std::string("\x01", 1), std::string(reinterpret_cast<char*>(&data), 1));

    encode_int<little, uint8_t>(reinterpret_cast<uint8_t*>(&data), 0x01);
    EXPECT_EQ(std::string("\x01", 1), std::string(reinterpret_cast<char*>(&data), 1));

    encode_int<big, int8_t>(reinterpret_cast<uint8_t*>(&data), 0x01);
    EXPECT_EQ(std::string("\x01", 1), std::string(reinterpret_cast<char*>(&data), 1));

    encode_int<big, uint8_t>(reinterpret_cast<uint8_t*>(&data), 0x01);
    EXPECT_EQ(std::string("\x01", 1), std::string(reinterpret_cast<char*>(&data), 1));
}

TEST(encoding_ints, int16)
{
    uint16_t data;

    encode_int<native, int16_t>(reinterpret_cast<uint8_t*>(&data), 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    encode_int<native, uint16_t>(reinterpret_cast<uint8_t*>(&data), 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    encode_int<little, int16_t>(reinterpret_cast<uint8_t*>(&data), 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    encode_int<little, uint16_t>(reinterpret_cast<uint8_t*>(&data), 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    encode_int<big, int16_t>(reinterpret_cast<uint8_t*>(&data), 0x0102);
    EXPECT_EQ(std::string("\x01\x02", 2), std::string(reinterpret_cast<char*>(&data), 2));

    encode_int<big, uint16_t>(reinterpret_cast<uint8_t*>(&data), 0x0102);
    EXPECT_EQ(std::string("\x01\x02", 2), std::string(reinterpret_cast<char*>(&data), 2));
}

TEST(encoding_ints, int32)
{
    uint32_t data;

    encode_int<native, int32_t>(reinterpret_cast<uint8_t*>(&data), 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    encode_int<native, uint32_t>(reinterpret_cast<uint8_t*>(&data), 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    encode_int<little, int32_t>(reinterpret_cast<uint8_t*>(&data), 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    encode_int<little, uint32_t>(reinterpret_cast<uint8_t*>(&data), 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    encode_int<big, int32_t>(reinterpret_cast<uint8_t*>(&data), 0x01020304);
    EXPECT_EQ(std::string("\x01\x02\x03\x04", 4), std::string(reinterpret_cast<char*>(&data), 4));

    encode_int<big, uint32_t>(reinterpret_cast<uint8_t*>(&data), 0x01020304);
    EXPECT_EQ(std::string("\x01\x02\x03\x04", 4), std::string(reinterpret_cast<char*>(&data), 4));
}

TEST(encoding_ints, int64)
{
    uint64_t data;

    encode_int<native, int64_t>(reinterpret_cast<uint8_t*>(&data), 0x0102030405060708ULL);
    EXPECT_EQ(std::string("\x08\x07\x06\x05\x04\x03\x02\x01", 8), std::string(reinterpret_cast<char*>(&data), 8));

    encode_int<native, uint64_t>(reinterpret_cast<uint8_t*>(&data), 0x0102030405060708ULL);
    EXPECT_EQ(std::string("\x08\x07\x06\x05\x04\x03\x02\x01", 8), std::string(reinterpret_cast<char*>(&data), 8));

    encode_int<little, int64_t>(reinterpret_cast<uint8_t*>(&data), 0x0102030405060708ULL);
    EXPECT_EQ(std::string("\x08\x07\x06\x05\x04\x03\x02\x01", 8), std::string(reinterpret_cast<char*>(&data), 8));

    encode_int<little, uint64_t>(reinterpret_cast<uint8_t*>(&data), 0x0102030405060708ULL);
    EXPECT_EQ(std::string("\x08\x07\x06\x05\x04\x03\x02\x01", 8), std::string(reinterpret_cast<char*>(&data), 8));

    encode_int<big, int64_t>(reinterpret_cast<uint8_t*>(&data), 0x0102030405060708ULL);
    EXPECT_EQ(std::string("\x01\x02\x03\x04\x05\x06\x07\x08", 8), std::string(reinterpret_cast<char*>(&data), 8));

    encode_int<big, uint64_t>(reinterpret_cast<uint8_t*>(&data), 0x0102030405060708ULL);
    EXPECT_EQ(std::string("\x01\x02\x03\x04\x05\x06\x07\x08", 8), std::string(reinterpret_cast<char*>(&data), 8));
}
