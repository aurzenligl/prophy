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
    std::vector<uint8_t> big = to_vector(
        "\x01\x00\x00\x02"
    );
    std::vector<uint8_t> little = to_vector(
        "\x01\x00\x02\x00"
    );

    std::vector<uint8_t> input(am_i_little ? big : little);
    std::vector<uint8_t> expected(am_i_little ? little : big);

    Scalar* next = prophy::swap(*reinterpret_cast<Scalar*>(input.data()));

    EXPECT_EQ(byte_distance(input.data(), next), 4);
    EXPECT_THAT(input, ContainerEq(expected));
}

TEST(generated, ScalarFixedArray)
{
    std::vector<uint8_t> big = to_vector(
        "\x00\x02"
        "\x00\x02"
        "\x00\x02"
    );
    std::vector<uint8_t> little = to_vector(
        "\x02\x00"
        "\x02\x00"
        "\x02\x00"
    );

    std::vector<uint8_t> input(am_i_little ? big : little);
    std::vector<uint8_t> expected(am_i_little ? little : big);

    ScalarFixedArray* next = prophy::swap(*reinterpret_cast<ScalarFixedArray*>(input.data()));

    EXPECT_EQ(byte_distance(input.data(), next), 6);
    EXPECT_THAT(input, ContainerEq(expected));
}

TEST(generated, Composite)
{
    std::vector<uint8_t> big = to_vector(
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02"
    );
    std::vector<uint8_t> little = to_vector(
        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
    );

    std::vector<uint8_t> input(am_i_little ? big : little);
    std::vector<uint8_t> expected(am_i_little ? little : big);

    Composite* next = prophy::swap(*reinterpret_cast<Composite*>(input.data()));

    EXPECT_EQ(byte_distance(input.data(), next), 8);
    EXPECT_THAT(input, ContainerEq(expected));
}

TEST(generated, CompositeFixedArray)
{
    std::vector<uint8_t> big = to_vector(
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02"
    );
    std::vector<uint8_t> little = to_vector(
        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
    );

    std::vector<uint8_t> input(am_i_little ? big : little);
    std::vector<uint8_t> expected(am_i_little ? little : big);

    CompositeFixedArray* next = prophy::swap(*reinterpret_cast<CompositeFixedArray*>(input.data()));

    EXPECT_EQ(byte_distance(input.data(), next), 12);
    EXPECT_THAT(input, ContainerEq(expected));
}
