#include <vector>
#include <gtest/gtest.h>
#include "generated/Paddings.pp.hpp"

using namespace testing;

TEST(generated_paddings, Endpad)
{
    std::vector<char> data(1024);

    Endpad x;
    x.x = 1;
    x.y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x02" "\x00",
            4), std::string(data.data(), size));
}
