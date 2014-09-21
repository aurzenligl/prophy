#include <vector>
#include <gtest/gtest.h>
#include "generated/Paddings.pp.hpp"
#include "util.hpp"

using namespace testing;

TEST(generated_paddings, Endpad)
{
    std::vector<char> data(1024);

    Endpad x;
    x.x = 1;
    x.y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x02" "\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03\x00\x04" "\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(4, x.y);
}

TEST(generated_paddings, EndpadFixed)
{
    std::vector<char> data(1024);

    EndpadFixed x;
    x.x = 1;
    x.y[0] = 2;
    x.y[1] = 3;
    x.y[2] = 4;
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02\x03\x04" "\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x05\x00\x00\x00\x06\x07\x08" "\x00")));
    EXPECT_EQ(5, x.x);
    EXPECT_EQ(6, x.y[0]);
    EXPECT_EQ(7, x.y[1]);
    EXPECT_EQ(8, x.y[2]);
}

TEST(generated_paddings, EndpadDynamic)
{
    std::vector<char> data(1024);

    EndpadDynamic x;
    x.x.push_back(2);
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02" "\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x02\x00\x00\x00\x03\x04" "\x00\x00")));
    EXPECT_EQ(2, x.x.size());
    EXPECT_EQ(3, x.x[0]);
    EXPECT_EQ(4, x.x[1]);
}

TEST(generated_paddings, EndpadLimited)
{
    std::vector<char> data(1024);

    EndpadLimited x;
    x.x.push_back(2);
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02" "\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x01\x00\x00\x00\x06" "\x00\x00\x00")));
    EXPECT_EQ(1, x.x.size());
    EXPECT_EQ(6, x.x[0]);
}

TEST(generated_paddings, EndpadGreedy)
{
    std::vector<char> data(1024);

    EndpadGreedy x;
    x.x = 1;
    x.y.push_back(2);
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00\x02" "\x00\x00\x00"),
            bytes(data.data(), size));

    /// * WARNING * If you're using greedy array of elements of smaller alignment than message
    /// you may receive different array than you sent.

    EXPECT_TRUE(x.decode(bytes(
            "\x05\x00\x00\x00\x06\x07\x00\x00")));
    EXPECT_EQ(5, x.x);
    EXPECT_EQ(4, x.y.size());
    EXPECT_EQ(6, x.y[0]);
    EXPECT_EQ(7, x.y[1]);
    EXPECT_EQ(0, x.y[2]);
    EXPECT_EQ(0, x.y[3]);
}

TEST(generated_paddings, Scalarpad)
{
    std::vector<char> data(1024);

    Scalarpad x;
    x.x = 1;
    x.y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00" "\x02\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ScalarpadComppre)
{
    std::vector<char> data(1024);

    ScalarpadComppre x;
    x.x.x = 1;
    x.y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00" "\x02\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ScalarpadComppost)
{
    std::vector<char> data(1024);

    ScalarpadComppost x;
    x.x = 1;
    x.y.x = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00" "\x02\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, UnionpadOptionalboolpad)
{
    std::vector<char> data(1024);

    UnionpadOptionalboolpad x;
    x.x = 1;
    x.has_y = true;
    x.y = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, UnionpadOptionalvaluepad)
{
    std::vector<char> data(1024);

    UnionpadOptionalvaluepad x;
    x.has_x = true;
    x.x = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00" "\x00\x00\x00\x00"
            "\x02\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, UnionpadDiscpad)
{
    std::vector<char> data(1024);

    UnionpadDiscpad x;
    x.x = 1;
    x.y.discriminator = UnionpadDiscpad_Helper::discriminator_a;
    x.y.a = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, UnionpadArmpad)
{
    std::vector<char> data(1024);

    UnionpadArmpad x;
    x.x = 1;
    x.y.discriminator = UnionpadArmpad_Helper::discriminator_a;
    x.y.a = 2;
    size_t size = x.encode(data.data());

    EXPECT_EQ(24, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00\x00\x00\x00\x00"
            "\x01\x00\x00\x00" "\x00\x00\x00\x00"
            "\x02" "\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ArraypadCounter)
{
    std::vector<char> data(1024);

    ArraypadCounter x;
    x.x.push_back(2);
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00" "\x02\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ArraypadCounterSeparated)
{
    std::vector<char> data(1024);

    ArraypadCounterSeparated x;
    x.y = 2;
    x.x.push_back(3);
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00"
            "\x02\x00\x00\x00"
            "\x03\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ArraypadCounterAligns)
{
    std::vector<char> data(1024);

    ArraypadCounterAligns x;
    x.x = 1;
    x.y.x.push_back(2);
    size_t size = x.encode(data.data());

    EXPECT_EQ(6, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00"
            "\x01\x00\x02" "\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ArraypadFixed)
{
    std::vector<char> data(1024);

    ArraypadFixed x;
    x.x = 1;
    x.y[0] = 2;
    x.y[1] = 3;
    x.y[2] = 4;
    x.z = 5;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x02\x03\x04" "\x00"
            "\x05\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ArraypadDynamic)
{
    std::vector<char> data(1024);

    ArraypadDynamic x;
    x.x.push_back(2);
    x.y = 3;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"
            "\x03\x00\x00\x00"),
            bytes(data.data(), size));
}

TEST(generated_paddings, ArraypadLimited)
{
    std::vector<char> data(1024);

    ArraypadLimited x;
    x.x.push_back(2);
    x.y = 3;
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"
            "\x03\x00\x00\x00"),
            bytes(data.data(), size));
}
