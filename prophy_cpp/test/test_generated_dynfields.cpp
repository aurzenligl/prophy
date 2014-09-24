#include <vector>
#include <gtest/gtest.h>
#include "generated/Dynfields.pp.hpp"
#include "util.hpp"

using namespace testing;

TEST(generated_dynfields, Dynfields)
{
    std::vector<char> data(1024);

    Dynfields x;
    x.x.push_back(2);
    x.y.push_back(3);
    x.z = 4;
    size_t size = x.encode(data.data());

    EXPECT_EQ(24, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02" "\x00"
            "\x01\x00\x03\x00" "\x00\x00\x00\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03\x00\x00\x00\x02\x02\x02" "\x00"
            "\x02\x00\x03\x00\x03\x00" "\x00\x00"
            "\x05\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_EQ(3, x.x.size());
    EXPECT_EQ(2, x.x[0]);
    EXPECT_EQ(2, x.x[1]);
    EXPECT_EQ(2, x.x[2]);
    EXPECT_EQ(2, x.y.size());
    EXPECT_EQ(3, x.y[0]);
    EXPECT_EQ(3, x.y[1]);
    EXPECT_EQ(5, x.z);
}

TEST(generated_dynfields, DynfieldsMixed)
{
    std::vector<char> data(1024);

    DynfieldsMixed x;
    x.x.push_back(2);
    x.y.push_back(3);
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x01\x00\x02" "\x00"
            "\x03\x00" "\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03\x00\x00\x00"
            "\x02\x00\x02\x02\x02" "\x00"
            "\x03\x00\x03\x00" "\x00\x00")));
    EXPECT_EQ(3, x.x.size());
    EXPECT_EQ(2, x.x[0]);
    EXPECT_EQ(2, x.x[1]);
    EXPECT_EQ(2, x.x[2]);
    EXPECT_EQ(2, x.y.size());
    EXPECT_EQ(3, x.y[0]);
    EXPECT_EQ(3, x.y[1]);
}

TEST(generated_dynfields, DynfieldsOverlapped)
{
    std::vector<char> data(1024);

    DynfieldsOverlapped x;
    x.a.push_back(4);
    x.a.push_back(5);
    x.b.push_back(2);
    x.c.push_back(3);
    size_t size = x.encode(data.data());

    EXPECT_EQ(24, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x02\x00\x00\x00\x01\x00\x00\x00"
            "\x02\x00" "\x00\x00" "\x01\x00\x00\x00"
            "\x03\x00\x04\x00\x05\x00" "\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x02\x00\x00\x00\x01\x00\x00\x00"
            "\x06\x00" "\x00\x00" "\x01\x00\x00\x00"
            "\x09\x00\x08\x00\x07\x00" "\x00\x00")));
    EXPECT_EQ(2, x.a.size());
    EXPECT_EQ(8, x.a[0]);
    EXPECT_EQ(7, x.a[1]);
    EXPECT_EQ(1, x.b.size());
    EXPECT_EQ(6, x.b[0]);
    EXPECT_EQ(1, x.c.size());
    EXPECT_EQ(9, x.c[0]);
}

TEST(generated_dynfields, DynfieldsPartialpad)
{
    std::vector<char> data(1024);

    DynfieldsPartialpad x;
    x.x = 1;
    x.y.x.push_back(2);
    x.y.y = 3;
    x.y.z = 4;
    size_t size = x.encode(data.data());

    EXPECT_EQ(32, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00\x00\x00\x00\x00"
            "\x01\x02" "\x00\x00\x00\x00\x00\x00"
            "\x03" "\x00\x00\x00\x00\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x02" "\x00\x00\x00\x00\x00\x00\x00"
            "\x01\x03" "\x00\x00\x00\x00\x00\x00"
            "\x04" "\x00\x00\x00\x00\x00\x00\x00"
            "\x05\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_EQ(2, x.x);
    EXPECT_EQ(1, x.y.x.size());
    EXPECT_EQ(3, x.y.x[0]);
    EXPECT_EQ(4, x.y.y);
    EXPECT_EQ(5, x.y.z);
}

TEST(generated_dynfields, DynfieldsScalarpartialpad)
{
    std::vector<char> data(1024);

    DynfieldsScalarpartialpad x;
    x.x.x.push_back(2);
    x.y.x.push_back(3);
    x.y.x.push_back(4);
    x.y.x.push_back(5);
    x.y.x.push_back(6);
    x.y.x.push_back(7);
    x.y.x.push_back(8);
    x.z.x.push_back(9);
    x.z.x.push_back(10);
    x.z.x.push_back(11);
    size_t size = x.encode(data.data());

    EXPECT_EQ(28, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02" "\x00\x00\x00"
            "\x06\x00\x00\x00\x03\x04\x05\x06\x07\x08" "\x00\x00"
            "\x03\x00\x00\x00\x09\x0a\x0b" "\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x02\x00\x00\x00" "\x02\x03" "\x00\x00"
            "\x02\x00\x00\x00" "\x04\x05" "\x00\x00"
            "\x05\x00\x00\x00" "abcde" "\x00\x00\x00")));
    EXPECT_EQ(bytes("\x02\x03"), x.x.x);
    EXPECT_EQ(bytes("\x04\x05"), x.y.x);
    EXPECT_EQ(bytes("abcde"), x.z.x);
}
