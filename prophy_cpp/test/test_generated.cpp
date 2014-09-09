#include <string>
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "generated/Arrays.pp.hpp"

using namespace testing;

TEST(generated, Builtin)
{
    std::string data(1024, 0);

    Builtin x;
    x.x = 1;
    x.y = 2;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string("\x01\x00\x00\x00\x02\x00\x00\x00", 8), std::string(data, 0, size));
}
