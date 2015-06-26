#include <gtest/gtest.h>
#include "util.hpp"
#include "Arrays.pp.hpp"

using namespace testing;

TEST(generated_raw_arrays, Builtin)
{
    test_swap<Builtin>(
        "\x01\x00\x00\x02",
        "\x01\x00\x02\x00"
    );
}

TEST(generated_raw_arrays, BuiltinFixed)
{
    test_swap<BuiltinFixed>(
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x02",

        "\xDD\xCC\xBB\xAA"
        "\x02\x00\x00\x00"
    );
}

TEST(generated_raw_arrays, BuiltinDynamic)
{
    test_swap<BuiltinDynamic>(
        "\x00\x00\x00\x03"
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x02"
        "\x00\x00\x00\x03",

        "\x03\x00\x00\x00"
        "\xDD\xCC\xBB\xAA"
        "\x02\x00\x00\x00"
        "\x03\x00\x00\x00"
    );
}

TEST(generated_raw_arrays, BuiltinLimited)
{
    test_swap<BuiltinLimited>(
        "\x00\x00\x00\x02"
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x02",

        "\x02\x00\x00\x00"
        "\xDD\xCC\xBB\xAA"
        "\x02\x00\x00\x00"
    );
}

TEST(generated_raw_arrays, BuiltinGreedy)
{
    test_swap<BuiltinGreedy>(
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x02",

        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x02",

        0
    );
}

TEST(generated_raw_arrays, Fixcomp)
{
    test_swap<Fixcomp>(
        "\x01\x00\x00\x02"
        "\x03\x00\x04\x00",

        "\x01\x00\x02\x00"
        "\x03\x00\x00\x04"
    );
}

TEST(generated_raw_arrays, FixcompFixed)
{
    test_swap<FixcompFixed>(
        "\x01\x00\x02\x00"
        "\x03\x00\x00\x04",

        "\x01\x00\x00\x02"
        "\x03\x00\x04\x00"
    );
}

TEST(generated_raw_arrays, FixcompDynamic)
{
    test_swap<FixcompDynamic>(
        "\x00\x00\x00\x04"
        "\x01\x00\x00\x01"
        "\x01\x00\x02\x00"
        "\x02\x00\x00\x01"
        "\x02\x00\x02\x00",

        "\x04\x00\x00\x00"
        "\x01\x00\x01\x00"
        "\x01\x00\x00\x02"
        "\x02\x00\x01\x00"
        "\x02\x00\x00\x02"
    );
}

TEST(generated_raw_arrays, FixcompLimited)
{
    test_swap<FixcompLimited>(
        "\x00\x00\x00\x01"
        "\x01\x00\x00\x01"
        "\xAA\xBB\xCC\xDD",

        "\x01\x00\x00\x00"
        "\x01\x00\x01\x00"
        "\xAA\xBB\xCC\xDD"
    );
}

TEST(generated_raw_arrays, FixcompGreedy)
{
    test_swap<FixcompGreedy>(
        "\x01\x00\x00\x01"
        "\x02\x00\x00\x02"
        "\x03\x00\x00\x03"
        "\x04\x00\x00\x04",

        "\x01\x00\x00\x01"
        "\x02\x00\x00\x02"
        "\x03\x00\x00\x03"
        "\x04\x00\x00\x04",

        0
    );
}

TEST(generated_raw_arrays, Dyncomp)
{
    test_swap<Dyncomp>(
        "\x00\x00\x00\x03"
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x01"
        "\x00\x00\x00\x02",

        "\x03\x00\x00\x00"
        "\xDD\xCC\xBB\xAA"
        "\x01\x00\x00\x00"
        "\x02\x00\x00\x00"
    );
}

TEST(generated_raw_arrays, DyncompDynamic)
{
    test_swap<DyncompDynamic>(
        "\x00\x00\x00\x02"
        "\x00\x00\x00\x01"
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x02"
        "\xAA\xBB\xCC\xDD"
        "\xAA\xBB\xCC\xDD",

        "\x02\x00\x00\x00"
        "\x01\x00\x00\x00"
        "\xDD\xCC\xBB\xAA"
        "\x02\x00\x00\x00"
        "\xDD\xCC\xBB\xAA"
        "\xDD\xCC\xBB\xAA"
    );
}

TEST(generated_raw_arrays, DyncompGreedy)
{
    test_swap<DyncompGreedy>(
        "\x00\x00\x00\x01"
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x02"
        "\xAA\xBB\xCC\xDD"
        "\xAA\xBB\xCC\xDD",

        "\x00\x00\x00\x01"
        "\xAA\xBB\xCC\xDD"
        "\x00\x00\x00\x02"
        "\xAA\xBB\xCC\xDD"
        "\xAA\xBB\xCC\xDD",

        0
    );
}
