#include <vector>
#include <gtest/gtest.h>
#include "generated/Others.pp.hpp"
#include "util.hpp"

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
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x02\x00"
            "\x03\x00\x04\x00"
            "\x01\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x07\x00\x08\x00"
            "\x09\x00\x01\x00"
            "\x01\x00\x00\x00")));
    EXPECT_EQ(7, x.a[0]);
    EXPECT_EQ(8, x.a[1]);
    EXPECT_EQ(9, x.a[2]);
    EXPECT_EQ(1, x.b);
    EXPECT_EQ(Enum_One, x.c);

    EXPECT_EQ(std::string(
            "a: 7\n"
            "a: 8\n"
            "a: 9\n"
            "b: 1\n"
            "c: Enum_One\n"), x.print());
}

TEST(generated_others, Floats)
{
    std::vector<char> data(1024);

    Floats x;
    x.a = 10;
    x.b = 10;
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x00\x00\x20\x41" "\x00\x00\x00\x00"
            "\x00\x00\x00\x00\x00\x00\x24\x40"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x00\x00\x20\x41" "\x00\x00\x00\x00"
            "\x00\x00\x00\x00\x00\x00\x24\x40")));
    EXPECT_EQ(10, x.a);
    EXPECT_EQ(10, x.b);
}

TEST(generated_others, BytesFixed)
{
    std::vector<char> data(1024);

    BytesFixed x;
    x.x[0] = 'a';
    x.x[1] = 'b';
    x.x[2] = 'c';
    size_t size = x.encode(data.data());

    EXPECT_EQ(3, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "abc"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "def")));
    EXPECT_EQ('d', x.x[0]);
    EXPECT_EQ('e', x.x[1]);
    EXPECT_EQ('f', x.x[2]);
}

TEST(generated_others, BytesDynamic)
{
    std::vector<char> data(1024);

    BytesDynamic x;
    x.x = bytes("abcd");
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x04\x00\x00\x00"
            "abcd"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x06\x00\x00\x00"
            "qwerty" "\x00\x00")));
    EXPECT_EQ(bytes("qwerty"), x.x);
}

TEST(generated_others, BytesLimited)
{
    std::vector<char> data(1024);

    BytesLimited x;
    x.x = bytes("ab");
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x02\x00\x00\x00"
            "ab\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03\x00\x00\x00"
            "abc\x00")));
    EXPECT_EQ(bytes("abc"), x.x);
}

TEST(generated_others, BytesGreedy)
{
    std::vector<char> data(1024);

    BytesGreedy x;
    x.x = bytes("abcde");
    size_t size = x.encode(data.data());

    EXPECT_EQ(5, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "abcde"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "qasw")));
    EXPECT_EQ(bytes("qasw"), x.x);
}
