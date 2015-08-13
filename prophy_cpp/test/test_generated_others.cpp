#include <vector>
#include <gtest/gtest.h>
#include "Others.ppf.hpp"
#include "util.hpp"

using namespace testing;
using namespace prophy::generated;

TEST(generated_others, ConstantTypedefEnum)
{
    std::vector<char> data(1024);

    ConstantTypedefEnum x{prophy::array<uint16_t, CONSTANT>{{1, 2, 3}}, 4, Enum_One};
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

TEST(generated_others, DynEnum)
{
    std::vector<char> data(1024);

    DynEnum x{{Enum_One, Enum_Two, static_cast<Enum>(3)}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x03\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x02\x00\x00\x00"
            "\x03\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03\x00\x00\x00"
            "\x03\x00\x00\x00"
            "\x02\x00\x00\x00"
            "\x01\x00\x00\x00")));
    EXPECT_EQ(3, x.x.size());
    EXPECT_EQ(static_cast<Enum>(3), x.x[0]);
    EXPECT_EQ(Enum_Two, x.x[1]);
    EXPECT_EQ(Enum_One, x.x[2]);

    EXPECT_EQ(std::string(
            "x: 3\n"
            "x: Enum_Two\n"
            "x: Enum_One\n"), x.print());
}

TEST(generated_others, Floats)
{
    std::vector<char> data(1024);

    Floats x{10, 10};
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

    x.a = -1.2;
    x.b = 12.567;

    EXPECT_EQ(std::string(
            "a: -1.2\n"
            "b: 12.567\n"), x.print());
}

TEST(generated_others, BytesFixed)
{
    std::vector<char> data(1024);

    BytesFixed x{prophy::array<uint8_t, 3>{{'a', 'b', 'c'}}};
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

    EXPECT_EQ(std::string(
            "x: 100\n"
            "x: 101\n"
            "x: 102\n"
            ), x.print());
}

TEST(generated_others, BytesDynamic)
{
    std::vector<char> data(1024);

    BytesDynamic x{{'a', 'b', 'c', 'd'}};
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

    x.x.clear();
    x.x.push_back(9);
    x.x.push_back(10);
    x.x.push_back(13);
    x.x.push_back(92);
    x.x.push_back(65);
    x.x.push_back(108);
    x.x.push_back(97);
    x.x.push_back(190);
    x.x.push_back(240);

    EXPECT_EQ(std::string(
        "x: 9\n"
        "x: 10\n"
        "x: 13\n"
        "x: 92\n"
        "x: 65\n"
        "x: 108\n"
        "x: 97\n"
        "x: 190\n"
        "x: 240\n"
        ), x.print());
}

TEST(generated_others, BytesLimited)
{
    std::vector<char> data(1024);

    BytesLimited x{{'a', 'b'}};
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

    EXPECT_EQ(std::string(
        "x: 97\n"
        "x: 98\n"
        "x: 99\n"
        ), x.print());
}

TEST(generated_others, BytesGreedy)
{
    std::vector<char> data(1024);

    BytesGreedy x{{'a', 'b', 'c', 'd', 'e'}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(5, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "abcde"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "qasw")));
    EXPECT_EQ(bytes("qasw"), x.x);

    EXPECT_EQ(std::string(
            "x: 113\n"
            "x: 97\n"
            "x: 115\n"
            "x: 119\n"
            ), x.print());
}
