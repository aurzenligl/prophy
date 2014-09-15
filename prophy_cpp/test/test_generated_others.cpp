#include <vector>
#include <gtest/gtest.h>
#include "generated/Others.pp.hpp"

using namespace testing;

TEST(generated_others, ConstantTypedefEnum)
{
    std::vector<char> data(1024);

    ConstantTypedefEnum x;
    x.a[0] = 1;
    x.a[1] = 2;
    x.a[2] = 3;
    x.b = 4;
    x.c = Enum_One;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x02\x00"
            "\x03\x00\x04\x00"
            "\x01\x00\x00\x00",
            size), std::string(data.data(), size));
}
