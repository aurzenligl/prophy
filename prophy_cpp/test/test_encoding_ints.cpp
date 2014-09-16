#include <string>
#include <gtest/gtest.h>
#include <prophy/detail/encoder.hpp>

using namespace testing;
using namespace prophy;
using namespace prophy::detail;

/// * WARNING * This test group assumes you're running on little endian machine.

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
