#include <vector>
#include <gtest/gtest.h>
#include "generated/Unions.pp.hpp"

using namespace testing;

TEST(generated_unions, Union)
{
    std::vector<char> data(1024);

    Union x;
    x.discriminator = Union::discriminator_a;
    x.a = 1;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00",
            12), std::string(data.data(), size));

    x.discriminator = Union::discriminator_b;
    x.b = 1;
    size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00",
            12), std::string(data.data(), size));

    x.discriminator = Union::discriminator_c;
    x.c.x = 1;
    x.c.y = 2;
    size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00",
            12), std::string(data.data(), size));
}

TEST(generated_unions, BuiltinOptional)
{
    std::vector<char> data(1024);

    BuiltinOptional x;
    x.has_x = false;
    x.x = 1;
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string(
            "\x00\x00\x00\x00\x00\x00\x00\x00",
            8), std::string(data.data(), size));

    x.has_x = true;
    x.x = 2;
    size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x02\x00\x00\x00",
            8), std::string(data.data(), size));
}

TEST(generated_unions, FixcompOptional)
{
    std::vector<char> data(1024);

    FixcompOptional x;
    x.has_x = false;
    x.x.x = 1;
    x.x.y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            12), std::string(data.data(), size));

    x.has_x = true;
    x.x.x = 3;
    x.x.y = 4;
    size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00",
            12), std::string(data.data(), size));
}
