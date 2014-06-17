#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "util.hpp"
#include "out/Scalar.hpp"
#include "out/ScalarFixedArray.hpp"
#include "out/Composite.hpp"
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
