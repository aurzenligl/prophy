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

TEST(generated, BuiltinFixed)
{
    std::string data(1024, 0);

    BuiltinFixed x;
    x.x[0] = 1;
    x.x[1] = 2;
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string("\x01\x00\x00\x00\x02\x00\x00\x00", 8), std::string(data, 0, size));
}

TEST(generated, BuiltinDynamic)
{
    std::string data(1024, 0);

    BuiltinDynamic x;
    x.x.push_back(1);
    x.x.push_back(2);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(12, size);
    EXPECT_EQ(std::string("\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00", 12), std::string(data, 0, size));
}

TEST(generated, BuiltinLimited)
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

TEST(generated, BuiltinGreedy)
{
    std::string data(1024, 0);

    BuiltinGreedy x;
    x.x.push_back(1);
    x.x.push_back(2);
    size_t size = x.encode(data.begin().base());

    EXPECT_EQ(8, size);
    EXPECT_EQ(std::string("\x01\x00\x00\x00\x02\x00\x00\x00", 8), std::string(data, 0, size));
}
