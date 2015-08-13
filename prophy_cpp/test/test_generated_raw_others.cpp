#include <gtest/gtest.h>
#include "util.hpp"
#include "Others.pp.hpp"

using namespace testing;

TEST(generated_raw_others, ConstantTypedefEnum)
{
    test_swap<ConstantTypedefEnum>(
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
}

TEST(generated_raw_others, EnumArrays)
{
    test_swap<EnumArrays>(
        "\x00\x00\x00\xF1"
        "\x00\x00\x00\xF2"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\xF3"
        "\x12\x34\x56\x78"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\xF4",

        "\xF1\x00\x00\x00"
        "\xF2\x00\x00\x00"
        "\x01\x00\x00\x00"
        "\xF3\x00\x00\x00"
        "\x12\x34\x56\x78"
        "\x01\x00\x00\x00"
        "\xF4\x00\x00\x00"
    );
}

TEST(generated_raw_others, EnumGreedyArray)
{
    test_swap<EnumGreedyArray>(
        "", ""
    );
}

TEST(generated_raw_others, EnumUnion)
{
    test_swap<EnumUnion>(
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x01",

        "\x01\x00\x00\x00"
        "\x01\x00\x00\x00"
    );
}
