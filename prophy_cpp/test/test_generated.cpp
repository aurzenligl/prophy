#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "util.hpp"
#include "out/Scalar.hpp"
#include "out/ScalarDynamicArray.hpp"
#include "out/ScalarFixedArray.hpp"
#include "out/ScalarGreedyArray.hpp"
#include "out/ScalarLimitedArray.hpp"
#include "out/Composite.hpp"
#include "out/CompositeDynamicArray.hpp"
#include "out/CompositeFixedArray.hpp"

using namespace testing;

TEST(generated, Scalar)
{
    data x(
        "\x01\x00\x00\x02",

        "\x01\x00\x02\x00"
    );

    Scalar* next = prophy::swap(*reinterpret_cast<Scalar*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ScalarDynamicArray)
{
    data x(
        "\x00\x00\x00\x03"
        "\x00\x05\x00\x06"
        "\x00\x07\xab\xcd",

        "\x03\x00\x00\x00"
        "\x05\x00\x06\x00"
        "\x07\x00\xab\xcd"
    );

    ScalarDynamicArray* next = prophy::swap(*reinterpret_cast<ScalarDynamicArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ScalarFixedArray)
{
    data x(
        "\x00\x02"
        "\x00\x02"
        "\x00\x02",

        "\x02\x00"
        "\x02\x00"
        "\x02\x00"
    );

    ScalarFixedArray* next = prophy::swap(*reinterpret_cast<ScalarFixedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 6);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ScalarGreedyArray)
{
    data x(
        "\x00\x08\x00\x00"
        "\xab\xcd\xef\xba",

        "\x08\x00\x00\x00"
        "\xab\xcd\xef\xba"
    );

    ScalarGreedyArray* next = prophy::swap(*reinterpret_cast<ScalarGreedyArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ScalarLimitedArray)
{
    data x(
        "\x00\x00\x00\x02"
        "\x00\x05\x00\x06"
        "\xab\xcd\xef\xba",

        "\x02\x00\x00\x00"
        "\x05\x00\x06\x00"
        "\xab\xcd\xef\xba"
    );

    ScalarLimitedArray* next = prophy::swap(*reinterpret_cast<ScalarLimitedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, Composite)
{
    data x(
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02",

        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
    );

    Composite* next = prophy::swap(*reinterpret_cast<Composite*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 8);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, CompositeDynamicArray)
{
    data x(
        "\x00\x00\x00\x03"
        "\x01\x00\x00\x01"
        "\x02\x00\x00\x02"
        "\x03\x00\x00\x03",

        "\x03\x00\x00\x00"
        "\x01\x00\x01\x00"
        "\x02\x00\x02\x00"
        "\x03\x00\x03\x00"
    );

    CompositeDynamicArray* next = prophy::swap(*reinterpret_cast<CompositeDynamicArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 16);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, CompositeFixedArray)
{
    data x(
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02",

        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
    );

    CompositeFixedArray* next = prophy::swap(*reinterpret_cast<CompositeFixedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}
