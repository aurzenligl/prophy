#include <string>
#include <gtest/gtest.h>
#include <prophy/detail/decoder.hpp>
#include "generated/Arrays.pp.hpp"
#include "generated/Dynfields.pp.hpp"
#include "util.hpp"

using namespace testing;
using namespace prophy;
using namespace prophy::detail;

TEST(encoding, decode_builtin_scalars)
{
    std::vector<uint8_t> data = bytes("\x01\x00\x00\x00");
    {
        const uint8_t* pos = data.data();
        const uint8_t* end = data.data() + data.size();
        uint32_t x = 0;

        EXPECT_TRUE(do_decode<native>(x, pos, end));
        EXPECT_EQ(data.data() + data.size(), pos);
        EXPECT_EQ(1, x);
    }
    {
        const uint8_t* pos = data.data() + 1;
        const uint8_t* end = data.data() + data.size();
        uint32_t x = 0;

        EXPECT_FALSE(do_decode<native>(x, pos, end));
        EXPECT_EQ(data.data() + 1, pos);
        EXPECT_EQ(0, x);
    }
}

TEST(encoding, decode_struct_failures)
{
    Builtin x;
    std::vector<uint8_t> data = bytes("\x01\x00\x00\x00\x02\x00\x00");

    EXPECT_FALSE(x.decode(data.data(), data.size()));
    EXPECT_EQ(1, x.x);
    EXPECT_EQ(0, x.y);

    data = bytes("\x03\x00\x00\x00\x04\x00\x00\x00\x00");

    EXPECT_FALSE(x.decode(data.data(), data.size()));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(4, x.y);

    data = bytes("\x05\x00\x00\x00");

    EXPECT_FALSE(x.decode(data.data(), data.size()));
    EXPECT_EQ(5, x.x);
    EXPECT_EQ(4, x.y);
}

TEST(encoding, endianness)
{
    size_t size;
    std::vector<char> data(1024);

    DynfieldsScalarpartialpad x;
    x.x.x = bytes("abc");
    x.y.x = bytes("d");
    x.z.x = bytes("efghi");

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
