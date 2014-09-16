#include <string>
#include <gtest/gtest.h>
#include <prophy/detail/encoder.hpp>

using namespace testing;

/// * WARNING * This test group assumes you're running on little endian machine.

TEST(encoding_ints, int16)
{
    uint16_t data;

    prophy::detail::number_encoder<prophy::native, int16_t>::encode(&data, 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    prophy::detail::number_encoder<prophy::native, uint16_t>::encode(&data, 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    prophy::detail::number_encoder<prophy::little, int16_t>::encode(&data, 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    prophy::detail::number_encoder<prophy::little, uint16_t>::encode(&data, 0x0102);
    EXPECT_EQ(std::string("\x02\x01", 2), std::string(reinterpret_cast<char*>(&data), 2));

    prophy::detail::number_encoder<prophy::big, int16_t>::encode(&data, 0x0102);
    EXPECT_EQ(std::string("\x01\x02", 2), std::string(reinterpret_cast<char*>(&data), 2));

    prophy::detail::number_encoder<prophy::big, uint16_t>::encode(&data, 0x0102);
    EXPECT_EQ(std::string("\x01\x02", 2), std::string(reinterpret_cast<char*>(&data), 2));
}

TEST(encoding_ints, int32)
{
    uint32_t data;

    prophy::detail::number_encoder<prophy::native, int32_t>::encode(&data, 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    prophy::detail::number_encoder<prophy::native, uint32_t>::encode(&data, 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    prophy::detail::number_encoder<prophy::little, int32_t>::encode(&data, 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    prophy::detail::number_encoder<prophy::little, uint32_t>::encode(&data, 0x01020304);
    EXPECT_EQ(std::string("\x04\x03\x02\x01", 4), std::string(reinterpret_cast<char*>(&data), 4));

    prophy::detail::number_encoder<prophy::big, int32_t>::encode(&data, 0x01020304);
    EXPECT_EQ(std::string("\x01\x02\x03\x04", 4), std::string(reinterpret_cast<char*>(&data), 4));

    prophy::detail::number_encoder<prophy::big, uint32_t>::encode(&data, 0x01020304);
    EXPECT_EQ(std::string("\x01\x02\x03\x04", 4), std::string(reinterpret_cast<char*>(&data), 4));
}
