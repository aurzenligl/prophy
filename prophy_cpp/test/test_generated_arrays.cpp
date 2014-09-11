#include <string>
#include <gtest/gtest.h>
#include "generated/Arrays.pp.hpp"

using namespace testing;

TEST(generated_arrays, Builtin)
{
    std::string data(1024, 0);

    Builtin x;
    x.x = 1;
    x.y = 2;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string("\x01\x00\x00\x00\x02\x00\x00\x00", 8), std::string(data, 0, size));
}

TEST(generated_arrays, BuiltinFixed)
{
    std::string data(1024, 0);

    BuiltinFixed x;
    x.x[0] = 1;
    x.x[1] = 2;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string("\x01\x00\x00\x00\x02\x00\x00\x00", 8), std::string(data, 0, size));
}

TEST(generated_arrays, BuiltinDynamic)
{
    std::string data(1024, 0);

    BuiltinDynamic x;
    x.x.push_back(1);
    x.x.push_back(2);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string("\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00", 12), std::string(data, 0, size));
}

TEST(generated_arrays, BuiltinLimited)
{
    std::string data(1024, 0);

    BuiltinLimited x;
    x.x.push_back(1);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string("\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00", 12), std::string(data, 0, size));

    x.x.push_back(2);
    x.x.push_back(3);
    size = x.encode(data.begin().base());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string("\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00", 12), std::string(data, 0, size));
}

TEST(generated_arrays, BuiltinGreedy)
{
    std::string data(1024, 0);

    BuiltinGreedy x;
    x.x.push_back(1);
    x.x.push_back(2);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string("\x01\x00\x00\x00\x02\x00\x00\x00", 8), std::string(data, 0, size));
}

TEST(generated_arrays, Fixcomp)
{
    std::string data(1024, 0);

    Fixcomp x;
    x.x.x = 1;
    x.x.y = 2;
    x.y.x = 3;
    x.y.y = 4;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(16, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00",
            16), std::string(data, 0, size));
}

TEST(generated_arrays, FixcompFixed)
{
    std::string data(1024, 0);

    FixcompFixed x;
    x.x[0].x = 1;
    x.x[0].y = 2;
    x.x[1].x = 3;
    x.x[1].y = 4;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(16, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00",
            16), std::string(data, 0, size));
}

TEST(generated_arrays, FixcompDynamic)
{
    std::string data(1024, 0);

    FixcompDynamic x;
    x.x.resize(2);
    x.x[0].x = 1;
    x.x[0].y = 2;
    x.x[1].x = 3;
    x.x[1].y = 4;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(20, size);
    EXPECT_EQ(std::string(
            "\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00",
            20), std::string(data, 0, size));
}

TEST(generated_arrays, FixcompLimited)
{
    std::string data(1024, 0);

    FixcompLimited x;
    x.x.resize(1);
    x.x[0].x = 1;
    x.x[0].y = 2;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(20, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00",
            20), std::string(data, 0, size));
}

TEST(generated_arrays, FixcompGreedy)
{
    std::string data(1024, 0);

    FixcompGreedy x;
    x.x.resize(2);
    x.x[0].x = 1;
    x.x[0].y = 2;
    x.x[1].x = 3;
    x.x[1].y = 4;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(16, size);
    EXPECT_EQ(std::string(
            "\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00",
            16), std::string(data, 0, size));
}

TEST(generated_arrays, Dyncomp)
{
    std::string data(1024, 0);

    Dyncomp x;
    x.x.x.push_back(1);
    x.x.x.push_back(2);
    x.x.x.push_back(3);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(16, size);
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00",
            16), std::string(data, 0, size));
}

TEST(generated_arrays, DyncompDynamic)
{
    std::string data(1024, 0);

    DyncompDynamic x;
    x.x.resize(2);
    x.x[0].x.push_back(1);
    x.x[0].x.push_back(2);
    x.x[0].x.push_back(3);
    x.x[1].x.push_back(4);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(28, size);
    EXPECT_EQ(std::string(
            "\x02\x00\x00\x00"
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00"
            "\x01\x00\x00\x00\x04\x00\x00\x00",
            28), std::string(data, 0, size));
}

TEST(generated_arrays, DyncompGreedy)
{
    std::string data(1024, 0);

    DyncompGreedy x;
    x.x.resize(2);
    x.x[0].x.push_back(1);
    x.x[0].x.push_back(2);
    x.x[0].x.push_back(3);
    x.x[1].x.push_back(4);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(24, size);
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00"
            "\x01\x00\x00\x00\x04\x00\x00\x00",
            24), std::string(data, 0, size));
}
