#include <string>
#include <gtest/gtest.h>
#include <prophy/detail/decoder.hpp>
#include "Arrays.ppf.hpp"
#include "Dynfields.ppf.hpp"
#include "Paddings.ppf.hpp"
#include "Unions.ppf.hpp"
#include "util.hpp"

using namespace testing;
using namespace prophy;
using namespace prophy::detail;
using namespace prophy::generated;

TEST(encoding, decode_struct_failures)
{
    Builtin x;

    EXPECT_FALSE(x.decode(bytes("\x01\x00\x02")));
    EXPECT_EQ(1, x.x);
    EXPECT_EQ(0, x.y);

    EXPECT_FALSE(x.decode(bytes("\x03\x00\x04\x00\x00\x00\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(4, x.y);

    EXPECT_FALSE(x.decode(bytes("\x05\x00")));
    EXPECT_EQ(5, x.x);
    EXPECT_EQ(4, x.y);
}

TEST(encoding, decode_dynamic_failures)
{
    BuiltinDynamic x;
    std::vector<uint8_t> data = bytes("\x01\x00\x00"); //not enough to decode counter

    EXPECT_FALSE(x.decode(data.data(), data.size()));
    EXPECT_EQ(0, x.x.size());

    data = bytes("\x01\x00\x00\x00"); // no array elements

    EXPECT_FALSE(x.decode(data.data(), data.size()));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(0, x.x[0]);

    data = bytes("\x01\x00\x00\x00\x02\x00\x00"); // one byte short

    EXPECT_FALSE(x.decode(data.data(), data.size()));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(0, x.x[0]);

    data = bytes("\x01\x00\x00\x00\x02\x00\x00\x00\x00"); // one byte too much

    EXPECT_FALSE(x.decode(data.data(), data.size()));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(2, x.x[0]);
}

TEST(encoding, decode_limited_failures)
{
    BuiltinLimited x;

    EXPECT_FALSE(x.decode(bytes("\x01\x00\x00\x00")));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(0, x.x[0]);

    EXPECT_FALSE(x.decode(bytes("\x01\x00\x00\x00\x01\x00\x00\x00")));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(1, x.x[0]);

    EXPECT_FALSE(x.decode(bytes("\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03")));
    EXPECT_EQ(2, x.x.size());
    EXPECT_EQ(1, x.x[0]);
    EXPECT_EQ(2, x.x[1]);

    x.x.clear();
    EXPECT_FALSE(x.decode(bytes("\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00")));
    EXPECT_EQ(0, x.x.size());
}

TEST(encoding, decode_greedy_failures)
{
    BuiltinGreedy x;

    EXPECT_FALSE(x.decode(bytes("\x01\x00\x00")));
    EXPECT_EQ(0, x.x.size());

    EXPECT_FALSE(x.decode(bytes("\x01\x00\x00\x00\x02")));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(1, x.x[0]);
}

TEST(encoding, decode_fixed_fixcomp_failures)
{
    FixcompFixed x;

    EXPECT_FALSE(x.decode(bytes("\x01\x00\x00\x00")));
    EXPECT_EQ(1, x.x[0].x);
    EXPECT_EQ(0, x.x[0].y);
    EXPECT_EQ(0, x.x[1].x);
    EXPECT_EQ(0, x.x[1].y);

    EXPECT_FALSE(x.decode(bytes("\x02\x00\x03\x00\x04\x00\x00")));
    EXPECT_EQ(2, x.x[0].x);
    EXPECT_EQ(3, x.x[0].y);
    EXPECT_EQ(4, x.x[1].x);
    EXPECT_EQ(0, x.x[1].y);

    EXPECT_FALSE(x.decode(bytes("\x04\x00\x05\x00\x06\x00\x07\x00\xFF")));
    EXPECT_EQ(4, x.x[0].x);
    EXPECT_EQ(5, x.x[0].y);
    EXPECT_EQ(6, x.x[1].x);
    EXPECT_EQ(7, x.x[1].y);
}

TEST(encoding, decode_greedy_dyncomp_failures)
{
    DyncompGreedy x;

    EXPECT_FALSE(x.decode(bytes("\x00")));
    EXPECT_EQ(0, x.x.size());

    EXPECT_FALSE(x.decode(bytes("\x00\x00\x00\x00\x00")));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(0, x.x[0].x.size());

    EXPECT_FALSE(x.decode(bytes("\x02\x00\x00\x00\x03\x00\x00\x00")));
    EXPECT_EQ(0, x.x.size());
}

TEST(encoding, decode_padding_failures)
{
    Endpad x;

    EXPECT_FALSE(x.decode(bytes("\x01\x00\x02")));
    EXPECT_EQ(1, x.x);
    EXPECT_EQ(2, x.y);

    EXPECT_FALSE(x.decode(bytes("\x03\x00\x04\x00\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(4, x.y);
}

TEST(encoding, decode_union_failures)
{
    Union x;

    EXPECT_FALSE(x.decode(bytes(
            "\x01\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00")));
    EXPECT_EQ(Union::discriminator_a, x.discriminator);

    EXPECT_FALSE(x.decode(bytes(
            "\x01\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_EQ(Union::discriminator_a, x.discriminator);
    EXPECT_EQ(4, x.a);

    EXPECT_FALSE(x.decode(bytes(
            "\x01\x00\x00\x00"
            "\x08\x00\x00\x00")));
    EXPECT_EQ(Union::discriminator_a, x.discriminator);
    EXPECT_EQ(8, x.a);

    EXPECT_FALSE(x.decode(bytes(
            "\x09\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00")));
}

TEST(encoding, decode_optional_failures)
{
    BuiltinOptional x;

    EXPECT_FALSE(x.decode(bytes(
            "\x01\x00\x00\x00"
            "\x01\x00\x00")));
    EXPECT_TRUE(x.x);

    EXPECT_FALSE(x.decode(bytes(
            "\x01\x00\x00\x00"
            "\x01\x00\x00\x00\x00")));
    EXPECT_TRUE(x.x);
    EXPECT_EQ(1, *x.x);

    EXPECT_FALSE(x.decode(bytes(
            "\x00\x00\x00\x00"
            "\x08\x00\x00")));
    EXPECT_FALSE(x.x);

    EXPECT_FALSE(x.decode(bytes(
            "\x00\x00\x00\x00"
            "\x08\x00\x00\x00\x00")));
    EXPECT_FALSE(x.x);
}

TEST(encoding, endianness)
{
    DynfieldsScalarpartialpad x;
    x.x.x = bytes("abc");
    x.y.x = bytes("d");
    x.z.x = bytes("efghi");

    EXPECT_EQ(bytes(
            "\x03\x00\x00\x00" "abc" "\x00"
            "\x01\x00\x00\x00" "d" "\x00\x00\x00"
            "\x05\x00\x00\x00" "efghi" "\x00\x00\x00"),
            x.encode<native>());

    EXPECT_EQ(bytes(
            "\x03\x00\x00\x00" "abc" "\x00"
            "\x01\x00\x00\x00" "d" "\x00\x00\x00"
            "\x05\x00\x00\x00" "efghi" "\x00\x00\x00"),
            x.encode<little>());

    EXPECT_EQ(bytes(
            "\x00\x00\x00\x03" "abc" "\x00"
            "\x00\x00\x00\x01" "d" "\x00\x00\x00"
            "\x00\x00\x00\x05" "efghi" "\x00\x00\x00"),
            x.encode<big>());

    EXPECT_TRUE(x.decode<native>(bytes(
            "\x01\x00\x00\x00" "a" "\x00\x00\x00"
            "\x02\x00\x00\x00" "bc" "\x00\x00"
            "\x03\x00\x00\x00" "def" "\x00")));
    EXPECT_EQ(bytes("a"), x.x.x);
    EXPECT_EQ(bytes("bc"), x.y.x);
    EXPECT_EQ(bytes("def"), x.z.x);

    EXPECT_TRUE(x.decode<little>(bytes(
            "\x01\x00\x00\x00" "a" "\x00\x00\x00"
            "\x02\x00\x00\x00" "bc" "\x00\x00"
            "\x03\x00\x00\x00" "def" "\x00")));
    EXPECT_EQ(bytes("a"), x.x.x);
    EXPECT_EQ(bytes("bc"), x.y.x);
    EXPECT_EQ(bytes("def"), x.z.x);

    EXPECT_TRUE(x.decode<big>(bytes(
            "\x00\x00\x00\x01" "a" "\x00\x00\x00"
            "\x00\x00\x00\x02" "bc" "\x00\x00"
            "\x00\x00\x00\x03" "def" "\x00")));
    EXPECT_EQ(bytes("a"), x.x.x);
    EXPECT_EQ(bytes("bc"), x.y.x);
    EXPECT_EQ(bytes("def"), x.z.x);
}
