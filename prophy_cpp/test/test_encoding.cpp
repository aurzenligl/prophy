#include <string>
#include <gtest/gtest.h>
#include "generated/Dynfields.pp.hpp"
#include "util.hpp"

using namespace testing;
using namespace prophy;

TEST(encoding, endianness)
{
    size_t size;
    std::vector<char> data(1024);

    DynfieldsScalarpartialpad x;
    x.x.x = genbytes("abc");
    x.y.x = genbytes("d");
    x.z.x = genbytes("efghi");

    size = x.encode<native>(data.data());
    EXPECT_EQ(28, size);
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00" "abc" "\x00"
            "\x01\x00\x00\x00" "d" "\x00\x00\x00"
            "\x05\x00\x00\x00" "efghi" "\x00\x00\x00",
            size), std::string(data.data(), size));

    size = x.encode<little>(data.data());
    EXPECT_EQ(28, size);
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00" "abc" "\x00"
            "\x01\x00\x00\x00" "d" "\x00\x00\x00"
            "\x05\x00\x00\x00" "efghi" "\x00\x00\x00",
            size), std::string(data.data(), size));

    size = x.encode<big>(data.data());
    EXPECT_EQ(28, size);
    EXPECT_EQ(std::string(
            "\x00\x00\x00\x03" "abc" "\x00"
            "\x00\x00\x00\x01" "d" "\x00\x00\x00"
            "\x00\x00\x00\x05" "efghi" "\x00\x00\x00",
            size), std::string(data.data(), size));
}
