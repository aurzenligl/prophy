#include <gtest/gtest.h>
#include "util.hpp"
#include "generated_raw/Others.ppr.hpp"

using namespace testing;
using namespace raw;

TEST(generated_raw_arrays, ConstantTypedefEnum)
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
