#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "util.hpp"
#include "generated_raw/Composite.pp.hpp"
#include "generated_raw/CompositeDynamicArray.pp.hpp"
#include "generated_raw/CompositeFixedArray.pp.hpp"
#include "generated_raw/CompositeGreedyArray.pp.hpp"
#include "generated_raw/CompositeLimitedArray.pp.hpp"
#include "generated_raw/ConstantTypedefEnum.pp.hpp"
#include "generated_raw/DynamicComposite.pp.hpp"
#include "generated_raw/DynamicCompositeComposite.pp.hpp"
#include "generated_raw/DynamicCompositeDynamicArray.pp.hpp"
#include "generated_raw/DynamicCompositeGreedyArray.pp.hpp"
#include "generated_raw/ManyArrays.pp.hpp"
#include "generated_raw/ManyArraysMixed.pp.hpp"
#include "generated_raw/ManyArraysMixedHeavily.pp.hpp"
#include "generated_raw/ManyArraysPadding.pp.hpp"
#include "generated_raw/ManyArraysTailFixed.pp.hpp"
#include "generated_raw/ManyDynamic.pp.hpp"
#include "generated_raw/Optional.pp.hpp"
#include "generated_raw/Scalar.pp.hpp"
#include "generated_raw/ScalarDynamicArray.pp.hpp"
#include "generated_raw/ScalarFixedArray.pp.hpp"
#include "generated_raw/ScalarGreedyArray.pp.hpp"
#include "generated_raw/ScalarLimitedArray.pp.hpp"
#include "generated_raw/Union.pp.hpp"

using namespace testing;

TEST(generated_raw, Composite)
{
    data x(
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02",

        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
    );

    Composite* next = prophy::swap(reinterpret_cast<Composite*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 8);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, CompositeDynamicArray)
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

    CompositeDynamicArray* next = prophy::swap(reinterpret_cast<CompositeDynamicArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 16);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, CompositeFixedArray)
{
    data x(
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02"
        "\x01\x00\x00\x02",

        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
        "\x01\x00\x02\x00"
    );

    CompositeFixedArray* next = prophy::swap(reinterpret_cast<CompositeFixedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, CompositeGreedyArray)
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

    CompositeGreedyArray* next = prophy::swap(reinterpret_cast<CompositeGreedyArray*>(x.input.data()));
    Composite* past_end = prophy::swap_n_fixed(
        prophy::cast<Composite*>(next), 2);

    EXPECT_EQ(byte_distance(x.input.data(), next), 2);
    EXPECT_EQ(byte_distance(x.input.data(), past_end), 18);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, CompositeLimitedArray)
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

    CompositeLimitedArray* next = prophy::swap(reinterpret_cast<CompositeLimitedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 14);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ConstantTypedefEnum)
{
    data x(
        "\x00\x01"
        "\x00\x02"
        "\x00\x03"
        "\x00\x04"
        "\x00\x00\x00\x01",

        "\x01\x00"
        "\x02\x00"
        "\x03\x00"
        "\x04\x00"
        "\x01\x00\x00\x00"
    );

    ConstantTypedefEnum* next = prophy::swap(reinterpret_cast<ConstantTypedefEnum*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, DynamicComposite)
{
    data x(
        "\x00\x00\x00\x03"
        "\x00\x01\x00\x02"
        "\x00\x03\xab\xcd",

        "\x03\x00\x00\x00"
        "\x01\x00\x02\x00"
        "\x03\x00\xab\xcd"
    );

    DynamicComposite* next = prophy::swap(reinterpret_cast<DynamicComposite*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, DynamicCompositeComposite)
{
    data x(
        "\x00\x00\x00\x03"
        "\x00\x01\x00\x02"
        "\x00\x03\xab\xcd"
        "\x00\x00\x00\x04"
        "\x00\x00\x00\x01"
        "\x00\x05\xab\xcd"
        "\x00\x00\x00\x02"
        "\x00\x06\x00\x07",

        "\x03\x00\x00\x00"
        "\x01\x00\x02\x00"
        "\x03\x00\xab\xcd"
        "\x04\x00\x00\x00"
        "\x01\x00\x00\x00"
        "\x05\x00\xab\xcd"
        "\x02\x00\x00\x00"
        "\x06\x00\x07\x00"
    );

    DynamicCompositeComposite* next = prophy::swap(reinterpret_cast<DynamicCompositeComposite*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 32);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, DynamicCompositeDynamicArray)
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

    DynamicCompositeDynamicArray* next = prophy::swap(reinterpret_cast<DynamicCompositeDynamicArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 24);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, DynamicCompositeGreedyArray)
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

    DynamicCompositeGreedyArray* next = prophy::swap(reinterpret_cast<DynamicCompositeGreedyArray*>(x.input.data()));
    DynamicComposite* past_end = prophy::swap_n_dynamic(
        prophy::cast<DynamicComposite*>(next), 2);

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_EQ(byte_distance(x.input.data(), past_end), 24);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ManyArrays)
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

    ManyArrays* next = prophy::swap(reinterpret_cast<ManyArrays*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 48);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ManyArraysMixed)
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

    ManyArraysMixed* next = prophy::swap(reinterpret_cast<ManyArraysMixed*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 16);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ManyArraysMixedHeavily)
{
    data x(
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x03"
        "\x00\x01\x00\x02"
        "\x00\x03\xab\xcd"
        "\x00\x00\x00\x05"
        "\x00\x04\x00\x05"
        "\x00\x06\x00\x07"
        "\x00\x08\xab\xcd"
        "\x00\x09\xab\xcd",

        "\x01\x00\x00\x00"
        "\x03\x00\x00\x00"
        "\x01\x00\x02\x00"
        "\x03\x00\xab\xcd"
        "\x05\x00\x00\x00"
        "\x04\x00\x05\x00"
        "\x06\x00\x07\x00"
        "\x08\x00\xab\xcd"
        "\x09\x00\xab\xcd"
    );

    ManyArraysMixedHeavily* next = prophy::swap(reinterpret_cast<ManyArraysMixedHeavily*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 36);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ManyArraysPadding)
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

    ManyArraysPadding* next = prophy::swap(reinterpret_cast<ManyArraysPadding*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 32);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ManyArraysTailFixed)
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

    ManyArraysTailFixed* next = prophy::swap(reinterpret_cast<ManyArraysTailFixed*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 24);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ManyDynamic)
{
    data x(
        "\x00\x00\x00\x01"
        "\x00\x01\xab\xcd"
        "\x00\x00\x00\x02"
        "\x00\x02\x00\x03"
        "\x00\x00\x00\x03"
        "\x00\x04\x00\x05"
        "\x00\x06\xab\xcd",

        "\x01\x00\x00\x00"
        "\x01\x00\xab\xcd"
        "\x02\x00\x00\x00"
        "\x02\x00\x03\x00"
        "\x03\x00\x00\x00"
        "\x04\x00\x05\x00"
        "\x06\x00\xab\xcd"
    );

    ManyDynamic* next = prophy::swap(reinterpret_cast<ManyDynamic*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 28);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, Optional)
{
    data x(
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x01"
        "\x02\x00\x00\x03"
        "\x04\x00\x00\x05",

        "\x01\x00\x00\x00"
        "\x01\x00\x00\x00"
        "\x01\x00\x00\x00"
        "\x02\x00\x03\x00"
        "\x04\x00\x05\x00"
    );

    Optional* next = prophy::swap(reinterpret_cast<Optional*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 20);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, Optional_not_set)
{
    data x(
        "\x00\x00\x00\x00"
        "\xab\xcd\xef\xab"
        "\x00\x00\x00\x00"
        "\xab\xcd\xef\xab"
        "\xab\xcd\xef\xab",

        "\x00\x00\x00\x00"
        "\xab\xcd\xef\xab"
        "\x00\x00\x00\x00"
        "\xab\xcd\xef\xab"
        "\xab\xcd\xef\xab"
    );

    Optional* next = prophy::swap(reinterpret_cast<Optional*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 20);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, Scalar)
{
    data x(
        "\x01\x00\x00\x02",

        "\x01\x00\x02\x00"
    );

    Scalar* next = prophy::swap(reinterpret_cast<Scalar*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ScalarDynamicArray)
{
    data x(
        "\x00\x00\x00\x03"
        "\x00\x05\x00\x06"
        "\x00\x07\xab\xcd",

        "\x03\x00\x00\x00"
        "\x05\x00\x06\x00"
        "\x07\x00\xab\xcd"
    );

    ScalarDynamicArray* next = prophy::swap(reinterpret_cast<ScalarDynamicArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ScalarFixedArray)
{
    data x(
        "\x00\x02"
        "\x00\x02"
        "\x00\x02",

        "\x02\x00"
        "\x02\x00"
        "\x02\x00"
    );

    ScalarFixedArray* next = prophy::swap(reinterpret_cast<ScalarFixedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 6);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ScalarGreedyArray)
{
    data x(
        "\x00\x08\xab\xcd"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x02",

        "\x08\x00\xab\xcd"
        "\x01\x00\x00\x00"
        "\x02\x00\x00\x00"
    );

    ScalarGreedyArray* next = prophy::swap(reinterpret_cast<ScalarGreedyArray*>(x.input.data()));
    uint32_t* past_end = prophy::swap_n_fixed(
        prophy::cast<uint32_t*>(next), 2);

    EXPECT_EQ(byte_distance(x.input.data(), next), 4);
    EXPECT_EQ(byte_distance(x.input.data(), past_end), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, ScalarLimitedArray)
{
    data x(
        "\x00\x00\x00\x02"
        "\x00\x05\x00\x06"
        "\xab\xcd\xef\xba",

        "\x02\x00\x00\x00"
        "\x05\x00\x06\x00"
        "\xab\xcd\xef\xba"
    );

    ScalarLimitedArray* next = prophy::swap(reinterpret_cast<ScalarLimitedArray*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 12);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, Union_a)
{
    data x(
        "\x00\x00\x00\x01"
        "\xab\xcd\xef\xab"
        "\x01\x00\x00\x00"
        "\x00\x00\x00\x00",

        "\x01\x00\x00\x00"
        "\xab\xcd\xef\xab"
        "\x01\x00\x00\x00"
        "\x00\x00\x00\x00"
    );

    Union* next = prophy::swap(reinterpret_cast<Union*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 16);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, Union_b)
{
    data x(
        "\x00\x00\x00\x02"
        "\xab\xcd\xef\xab"
        "\x00\x00\x00\x00"
        "\x00\x00\x00\x01",

        "\x02\x00\x00\x00"
        "\xab\xcd\xef\xab"
        "\x01\x00\x00\x00"
        "\x00\x00\x00\x00"
    );

    Union* next = prophy::swap(reinterpret_cast<Union*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 16);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}

TEST(generated_raw, Union_c)
{
    data x(
        "\x00\x00\x00\x03"
        "\xab\xcd\xef\xab"
        "\x01\x00\x00\x02"
        "\x03\x00\x00\x04",

        "\x03\x00\x00\x00"
        "\xab\xcd\xef\xab"
        "\x01\x00\x02\x00"
        "\x03\x00\x04\x00"
    );

    Union* next = prophy::swap(reinterpret_cast<Union*>(x.input.data()));

    EXPECT_EQ(byte_distance(x.input.data(), next), 16);
    EXPECT_THAT(x.input, ContainerEq(x.expected));
}
