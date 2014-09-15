#include <vector>
#include <gtest/gtest.h>
#include "generated/Dynfields.pp.hpp"

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
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x02" "\x00"
            "\x01\x00\x03\x00" "\x00\x00\x00\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00",
            size), std::string(data.data(), size));
}

TEST(generated_dynfields, DynfieldsMixed)
{
    std::vector<char> data(1024);

    DynfieldsMixed x;
    x.x.push_back(2);
    x.y.push_back(3);
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00"
            "\x01\x00\x02" "\x00"
            "\x03\x00" "\x00\x00",
            size), std::string(data.data(), size));
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
    EXPECT_EQ(std::string(
            "\x02\x00\x00\x00\x01\x00\x00\x00"
            "\x02\x00" "\x00\x00" "\x01\x00\x00\x00"
            "\x03\x00\x04\x00\x05\x00" "\x00\x00",
            size), std::string(data.data(), size));
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
    EXPECT_EQ(std::string(
            "\x01" "\x00\x00\x00\x00\x00\x00\x00"
            "\x01\x02" "\x00\x00\x00\x00\x00\x00"
            "\x03" "\x00\x00\x00\x00\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00",
            size), std::string(data.data(), size));
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
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x02" "\x00\x00\x00"
            "\x06\x00\x00\x00\x03\x04\x05\x06\x07\x08" "\x00\x00"
            "\x03\x00\x00\x00\x09\x0a\x0b" "\x00",
            size), std::string(data.data(), size));
}
