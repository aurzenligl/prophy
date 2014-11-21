#include <gtest/gtest.h>
#include "util.hpp"
#include "generated_raw/Others.pp.hpp"

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
