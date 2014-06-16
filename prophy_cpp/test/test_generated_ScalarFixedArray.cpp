#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "util.hpp"
#include "out/ScalarFixedArray.hpp"

using namespace testing;

TEST(generated, ScalarFixedArray)
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

    ScalarFixedArray* next = prophy::swap(*reinterpret_cast<ScalarFixedArray*>(input.data()));

    EXPECT_EQ(byte_distance(input.data(), next), 12);
    EXPECT_THAT(input, ContainerEq(expected));
}
