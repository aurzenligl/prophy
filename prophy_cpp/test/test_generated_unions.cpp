#include <vector>
#include <gtest/gtest.h>
#include "generated/Unions.pp.hpp"
#include "util.hpp"

using namespace testing;

TEST(generated_unions, Union)
{
    std::vector<char> data(1024);

    Union x;
    x.discriminator = Union::discriminator_a;
    x.a = 1;
    size_t size = x.encode(data.data());

    /// encoding
    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    x.discriminator = Union::discriminator_b;
    x.b = 1;
    size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(bytes(
            "\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    x.discriminator = Union::discriminator_c;
    x.c.x = 1;
    x.c.y = 2;
    size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(bytes(
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00"),
            bytes(data.data(), size));

    /// decoding
    EXPECT_TRUE(x.decode(bytes(
            "\x01\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_EQ(Union::discriminator_a, x.discriminator);
    EXPECT_EQ(4, x.a);

    EXPECT_TRUE(x.decode(bytes(
            "\x02\x00\x00\x00"
            "\x08\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_EQ(Union::discriminator_b, x.discriminator);
    EXPECT_EQ(8, x.b);

    EXPECT_TRUE(x.decode(bytes(
            "\x03\x00\x00\x00"
            "\x01\x00\x00\x00\x02\x00\x00\x00")));
    EXPECT_EQ(Union::discriminator_c, x.discriminator);
    EXPECT_EQ(1, x.c.x);
    EXPECT_EQ(2, x.c.y);
}

TEST(generated_unions, BuiltinOptional)
{
    std::vector<char> data(1024);

    BuiltinOptional x;
    x.has_x = false;
    x.x = 1;
    size_t size = x.encode(data.data());

    /// encoding
    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x00\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    x.has_x = true;
    x.x = 2;
    size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02\x00\x00\x00"),
            bytes(data.data(), size));

    /// decoding
    EXPECT_TRUE(x.decode(bytes(
            "\x00\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_FALSE(x.has_x);

    EXPECT_TRUE(x.decode(bytes(
            "\x01\x00\x00\x00\x05\x00\x00\x00")));
    EXPECT_TRUE(x.has_x);
    EXPECT_EQ(5, x.x);
}

TEST(generated_unions, FixcompOptional)
{
    std::vector<char> data(1024);

    FixcompOptional x;
    x.has_x = false;
    x.x.x = 1;
    x.x.y = 2;
    size_t size = x.encode(data.data());

    /// encoding
    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    x.has_x = true;
    x.x.x = 3;
    x.x.y = 4;
    size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00"),
            bytes(data.data(), size));

    /// decoding
    EXPECT_TRUE(x.decode(bytes(
            "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_FALSE(x.has_x);

    EXPECT_TRUE(x.decode(bytes(
            "\x01\x00\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00")));
    EXPECT_TRUE(x.has_x);
    EXPECT_EQ(7, x.x.x);
    EXPECT_EQ(8, x.x.y);
}
