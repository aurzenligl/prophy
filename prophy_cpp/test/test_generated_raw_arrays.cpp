#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "util.hpp"
#include "generated_raw/Arrays.ppr.hpp"

using namespace testing;
using namespace raw;

TEST(generated_raw_arrays, Builtin)
{
    data x(
        "\x01\x00\x00\x02",

        "\x01\x00\x02\x00"
    );

    Builtin* next = prophy::swap(reinterpret_cast<Builtin*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw_arrays, BuiltinFixed)
{
    data x(
        "\x00\x02"
        "\x00\x02"
        "\x00\x02",

        "\x02\x00"
        "\x02\x00"
        "\x02\x00"
    );

    BuiltinFixed* next = prophy::swap(reinterpret_cast<BuiltinFixed*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 6);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw_arrays, BuiltinDynamic)
{
    data x(
        "\x00\x00\x00\x03"
        "\x00\x05\x00\x06"
        "\x00\x07\xab\xcd",

        "\x03\x00\x00\x00"
        "\x05\x00\x06\x00"
        "\x07\x00\xab\xcd"
    );

    BuiltinDynamic* next = prophy::swap(reinterpret_cast<BuiltinDynamic*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw_arrays, BuiltinLimited)
{
    data x(
        "\x00\x00\x00\x02"
        "\x00\x05\x00\x06"
        "\xab\xcd\xef\xba",

        "\x02\x00\x00\x00"
        "\x05\x00\x06\x00"
        "\xab\xcd\xef\xba"
    );

    BuiltinLimited* next = prophy::swap(reinterpret_cast<BuiltinLimited*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw_arrays, BuiltinGreedy)
{
    data x(
        "\x00\x08\xab\xcd"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x02",

        "\x08\x00\xab\xcd"
        "\x01\x00\x00\x00"
        "\x02\x00\x00\x00"
    );

    BuiltinGreedy* next = prophy::swap(reinterpret_cast<BuiltinGreedy*>(x.input.data()));
    uint32_t* past_end = prophy::swap_n_fixed(
        prophy::cast<uint32_t*>(next), 2);

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_EQ(byte_distance(x.input.data(), past_end), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}
