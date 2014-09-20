#include <vector>
#include <gtest/gtest.h>
#include "generated/Arrays.pp.hpp"
#include "util.hpp"

using namespace testing;

TEST(generated_arrays, Builtin)
{
    std::vector<uint8_t> data(1024);

    Builtin x;
    x.x = 1;
    x.y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes("\x01\x00\x00\x00\x02\x00\x00\x00"), bytes(data.data(), size));

    data = bytes("\x03\x00\x00\x00\x04\x00\x00\x00");

    EXPECT_TRUE(x.decode(data.data(), data.size()));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(4, x.y);
}

TEST(generated_arrays, BuiltinFixed)
{
    std::vector<uint8_t> data(1024);

    BuiltinFixed x;
    x.x[0] = 1;
    x.x[1] = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes("\x01\x00\x00\x00\x02\x00\x00\x00"), bytes(data.data(), size));

    data = bytes("\x03\x00\x00\x00\x04\x00\x00\x00");

    EXPECT_TRUE(x.decode(data.data(), data.size()));
    EXPECT_EQ(3, x.x[0]);
    EXPECT_EQ(4, x.x[1]);
}

TEST(generated_arrays, BuiltinDynamic)
{
    std::vector<uint8_t> data(1024);

    BuiltinDynamic x;
    x.x.push_back(1);
    x.x.push_back(2);
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes("\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00"), bytes(data.data(), size));
}

TEST(generated_arrays, BuiltinLimited)
{
    std::vector<uint8_t> data(1024);

    BuiltinLimited x;
    x.x.push_back(1);
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes("\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00"), bytes(data.data(), size));

    x.x.push_back(2);
    x.x.push_back(3);
    size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes("\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00"), bytes(data.data(), size));
}

TEST(generated_arrays, BuiltinGreedy)
{
    std::vector<uint8_t> data(1024);

    BuiltinGreedy x;
    x.x.push_back(1);
    x.x.push_back(2);
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes("\x01\x00\x00\x00\x02\x00\x00\x00"), bytes(data.data(), size));
}

TEST(generated_arrays, Fixcomp)
{
    std::vector<uint8_t> data(1024);

    Fixcomp x;
    x.x.x = 1;
    x.x.y = 2;
    x.y.x = 3;
    x.y.y = 4;
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_arrays, FixcompFixed)
{
    std::vector<uint8_t> data(1024);

    FixcompFixed x;
    x.x[0].x = 1;
    x.x[0].y = 2;
    x.x[1].x = 3;
    x.x[1].y = 4;
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_arrays, FixcompDynamic)
{
    std::vector<uint8_t> data(1024);

    FixcompDynamic x;
    x.x.resize(2);
    x.x[0].x = 1;
    x.x[0].y = 2;
    x.x[1].x = 3;
    x.x[1].y = 4;
    size_t size = x.encode(data.data());

    EXPECT_EQ(20, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_arrays, FixcompLimited)
{
    std::vector<uint8_t> data(1024);

    FixcompLimited x;
    x.x.resize(1);
    x.x[0].x = 1;
    x.x[0].y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(20, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_arrays, FixcompGreedy)
{
    std::vector<uint8_t> data(1024);

    FixcompGreedy x;
    x.x.resize(2);
    x.x[0].x = 1;
    x.x[0].y = 2;
    x.x[1].x = 3;
    x.x[1].y = 4;
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_arrays, Dyncomp)
{
    std::vector<uint8_t> data(1024);

    Dyncomp x;
    x.x.x.push_back(1);
    x.x.x.push_back(2);
    x.x.x.push_back(3);
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_arrays, DyncompDynamic)
{
    std::vector<uint8_t> data(1024);

    DyncompDynamic x;
    x.x.resize(2);
    x.x[0].x.push_back(1);
    x.x[0].x.push_back(2);
    x.x[0].x.push_back(3);
    x.x[1].x.push_back(4);
    size_t size = x.encode(data.data());

    EXPECT_EQ(28, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x02\x00\x00\x00"
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00"
            "\x01\x00\x00\x00\x04\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_arrays, DyncompGreedy)
{
    std::vector<uint8_t> data(1024);

    DyncompGreedy x;
    x.x.resize(2);
    x.x[0].x.push_back(1);
    x.x[0].x.push_back(2);
    x.x[0].x.push_back(3);
    x.x[1].x.push_back(4);
    size_t size = x.encode(data.data());

    EXPECT_EQ(24, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x03\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00"
            "\x01\x00\x00\x00\x04\x00\x00\x00"),
            bytes(data.data(), size));
}
