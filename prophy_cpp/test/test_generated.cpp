#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "util.hpp"
#include "out/Scalar.hpp"
#include "out/ScalarDynamicArray.hpp"
#include "out/ScalarFixedArray.hpp"
#include "out/ScalarGreedyArray.hpp"
#include "out/ScalarLimitedArray.hpp"
#include "out/DynamicComposite.hpp"
#include "out/DynamicCompositeDynamicArray.hpp"
#include "out/DynamicCompositeGreedyArray.hpp"
#include "out/ManyArrays.hpp"
#include "out/ManyArraysMixed.hpp"
#include "out/ManyArraysPadding.hpp"
#include "out/ManyArraysTailFixed.hpp"
#include "out/Composite.hpp"
#include "out/CompositeDynamicArray.hpp"
#include "out/CompositeFixedArray.hpp"
#include "out/CompositeGreedyArray.hpp"
#include "out/CompositeLimitedArray.hpp"

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
        "\x00\x08\xab\xcd"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x02",

        "\x08\x00\xab\xcd"
        "\x01\x00\x00\x00"
        "\x02\x00\x00\x00"
    );

    ScalarGreedyArray* next = prophy::swap(*reinterpret_cast<ScalarGreedyArray*>(x.input.data()));
    uint32_t* past_end = prophy::swap_n_fixed(
        prophy::cast<uint32_t*>(next), 2);

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_EQ(byte_distance(x.input.data(), past_end), 12);
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

TEST(generated, DynamicComposite)
{
    data x(
        "\x00\x00\x00\x03"
        "\x00\x01\x00\x02"
        "\x00\x03\xab\xcd",

        "\x03\x00\x00\x00"
        "\x01\x00\x02\x00"
        "\x03\x00\xab\xcd"
    );

    DynamicComposite* next = prophy::swap(*reinterpret_cast<DynamicComposite*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, DynamicCompositeDynamicArray)
{
    data x(
        "\x00\x02\xab\xcd"
        "\x00\x00\x00\x01"
        "\x00\x01\xef\xab"
        "\x00\x00\x00\x03"
        "\x00\x01\x00\x02"
        "\x00\x03\xab\xcd",

        "\x02\x00\xab\xcd"
        "\x01\x00\x00\x00"
        "\x01\x00\xef\xab"
        "\x03\x00\x00\x00"
        "\x01\x00\x02\x00"
        "\x03\x00\xab\xcd"
    );

    DynamicCompositeDynamicArray* next = prophy::swap(*reinterpret_cast<DynamicCompositeDynamicArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 24);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, DynamicCompositeGreedyArray)
{
    data x(
        "\x00\x01\xab\xcd"
        "\x00\x00\x00\x01"
        "\x00\x01\xef\xab"
        "\x00\x00\x00\x03"
        "\x00\x01\x00\x02"
        "\x00\x03\xab\xcd",

        "\x01\x00\xab\xcd"
        "\x01\x00\x00\x00"
        "\x01\x00\xef\xab"
        "\x03\x00\x00\x00"
        "\x01\x00\x02\x00"
        "\x03\x00\xab\xcd"
    );

    DynamicCompositeGreedyArray* next = prophy::swap(*reinterpret_cast<DynamicCompositeGreedyArray*>(x.input.data()));
    DynamicComposite* past_end = prophy::swap_n_dynamic(
        prophy::cast<DynamicComposite*>(next), 2);

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_EQ(byte_distance(x.input.data(), past_end), 24);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ManyArrays)
{
    data x(
        "\x00\x00\x00\x05"
        "\x01\x02\x03\x04"
        "\x05\xab"
        "\x00\x02\x00\x01"
        "\x00\x02"
        "\x03\xab\xab\xab\xab\xab\xab\xab"
        "\x00\x00\x00\x00\x00\x00\x00\x01"
        "\x00\x00\x00\x00\x00\x00\x00\x02"
        "\x00\x00\x00\x00\x00\x00\x00\x03",

        "\x05\x00\x00\x00"
        "\x01\x02\x03\x04"
        "\x05\xab"
        "\x02\x00\x01\x00"
        "\x02\x00"
        "\x03\xab\xab\xab\xab\xab\xab\xab"
        "\x01\x00\x00\x00\x00\x00\x00\x00"
        "\x02\x00\x00\x00\x00\x00\x00\x00"
        "\x03\x00\x00\x00\x00\x00\x00\x00"
    );

    ManyArrays* next = prophy::swap(*reinterpret_cast<ManyArrays*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 48);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ManyArraysMixed)
{
    data x(
        "\x00\x00\x00\x05"
        "\x00\x02"
        "\x01\x02\x03\x04"
        "\x05\x00"
        "\x00\x01\x00\x02",

        "\x05\x00\x00\x00"
        "\x02\x00"
        "\x01\x02\x03\x04"
        "\x05\x00"
        "\x01\x00\x02\x00"
    );

    ManyArraysMixed* next = prophy::swap(*reinterpret_cast<ManyArraysMixed*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 16);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ManyArraysPadding)
{
    data x(
        "\x01\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x02\x02\x03\x00"
        "\x00\x00\x00\x02"
        "\x04\x05\x00\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x06",

        "\x01\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x02\x02\x03\x00"
        "\x02\x00\x00\x00"
        "\x04\x05\x00\x00"
        "\x00\x00\x00\x00"
        "\x06\x00\x00\x00"
        "\x00\x00\x00\x00"
    );

    ManyArraysPadding* next = prophy::swap(*reinterpret_cast<ManyArraysPadding*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 32);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, ManyArraysTailFixed)
{
    data x(
        "\x02\x02\x03\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x04"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x05",

        "\x02\x02\x03\x00"
        "\x00\x00\x00\x00"
        "\x04\x00\x00\x00"
        "\x00\x00\x00\x00"
        "\x05\x00\x00\x00"
        "\x00\x00\x00\x00"
    );

    ManyArraysTailFixed* next = prophy::swap(*reinterpret_cast<ManyArraysTailFixed*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 24);
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

TEST(generated, CompositeGreedyArray)
{
    data x(
        "\x00\x01"
        "\x01\x00\x00\x01"
        "\x02\x00\x00\x02"
        "\x01\x00\x00\x01"
        "\x02\x00\x00\x02",

        "\x01\x00"
        "\x01\x00\x01\x00"
        "\x02\x00\x02\x00"
        "\x01\x00\x01\x00"
        "\x02\x00\x02\x00"
    );

    CompositeGreedyArray* next = prophy::swap(*reinterpret_cast<CompositeGreedyArray*>(x.input.data()));
    Composite* past_end = prophy::swap_n_fixed(
        prophy::cast<Composite*>(next), 2);

    EXPECT_EQ(byte_distance(x.input.data(), next), 2);
    EXPECT_EQ(byte_distance(x.input.data(), past_end), 18);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated, CompositeLimitedArray)
{
    data x(
        "\x00\x02"
        "\x01\x00\x00\x01"
        "\x02\x00\x00\x02"
        "\xab\xcd\xef\xba",

        "\x02\x00"
        "\x01\x00\x01\x00"
        "\x02\x00\x02\x00"
        "\xab\xcd\xef\xba"
    );

    CompositeLimitedArray* next = prophy::swap(*reinterpret_cast<CompositeLimitedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 14);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}
