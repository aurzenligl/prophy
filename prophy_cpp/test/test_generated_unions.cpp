#include <string>
#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include "generated/Unions.pp.hpp"

using namespace testing;

TEST(generated_unions, Union)
{
    std::string data(1024, 0);

    Union x;
    x.discriminator = Union::discriminator_a;
    x.a = 1;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00",
            12), std::string(data, 0, size));

    x.discriminator = Union::discriminator_b;
    x.b = 1;
    size = x.encode(data.begin().base());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00",
            12), std::string(data, 0, size));

    x.discriminator = Union::discriminator_c;
    x.c.x = 1;
    x.c.y = 2;
    size = x.encode(data.begin().base());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00",
            12), std::string(data, 0, size));
}
