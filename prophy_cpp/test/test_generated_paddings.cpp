#include <vector>
#include <gtest/gtest.h>
#include "Paddings.ppf.hpp"
#include "util.hpp"

using namespace testing;
using namespace prophy::generated;

TEST(generated_paddings, Endpad)
{
    std::vector<char> data(1024);

    Endpad x{1, 2};
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

    EndpadFixed x{1, prophy::array<uint8_t, 3>{{2, 3, 4}}};
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

    EndpadDynamic x{{2}};
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

    EndpadLimited x{{2}};
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

    EndpadGreedy x{1, {2}};
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

    Scalarpad x{1, 2};
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00" "\x02\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03" "\x00" "\x04\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(4, x.y);
}

TEST(generated_paddings, ScalarpadComppre)
{
    std::vector<char> data(1024);

    ScalarpadComppre x{{1}, 2};
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00" "\x02\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03" "\x00" "\x04\x00")));
    EXPECT_EQ(3, x.x.x);
    EXPECT_EQ(4, x.y);
}

TEST(generated_paddings, ScalarpadComppost)
{
    std::vector<char> data(1024);

    ScalarpadComppost x{1, {2}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(4, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00" "\x02\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03" "\x00" "\x04\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(4, x.y.x);
}

TEST(generated_paddings, UnionpadOptionalboolpad)
{
    std::vector<char> data(1024);

    UnionpadOptionalboolpad x{1, 2};
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03" "\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x04" "\x00\x00\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_TRUE(x.y);
    EXPECT_EQ(4, *x.y);
}

TEST(generated_paddings, UnionpadOptionalvaluepad)
{
    std::vector<char> data(1024);

    UnionpadOptionalvaluepad x{2};
    size_t size = x.encode(data.data());

    EXPECT_EQ(16, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00" "\x00\x00\x00\x00"
            "\x02\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x01\x00\x00\x00" "\x00\x00\x00\x00"
            "\x03\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_TRUE(x.x);
    EXPECT_EQ(3, *x.x);
}

TEST(generated_paddings, UnionpadDiscpad)
{
    std::vector<char> data(1024);

    UnionpadDiscpad x{1, {UnionpadDiscpad_Helper::discriminator_a_t, 2}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03" "\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x04" "\x00\x00\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(UnionpadDiscpad_Helper::discriminator_a, x.y.discriminator);
    EXPECT_EQ(4, x.y.a);
}

TEST(generated_paddings, UnionpadArmpad)
{
    std::vector<char> data(1024);

    UnionpadArmpad x{1, {UnionpadArmpad_Helper::discriminator_a_t, 2}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(24, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00\x00\x00\x00\x00"
            "\x01\x00\x00\x00" "\x00\x00\x00\x00"
            "\x02" "\x00\x00\x00\x00\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03" "\x00\x00\x00\x00\x00\x00\x00"
            "\x02\x00\x00\x00" "\x00\x00\x00\x00"
            "\x04\x00\x00\x00\x00\x00\x00\x00")));
    EXPECT_EQ(3, x.x);
    EXPECT_EQ(UnionpadArmpad_Helper::discriminator_b, x.y.discriminator);
    EXPECT_EQ(4, x.y.b);
}

TEST(generated_paddings, ArraypadCounter)
{
    std::vector<char> data(1024);

    ArraypadCounter x{{2}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(8, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x02\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x03\x00\x00\x00"
            "\x02\x00\x00\x00"
            "\x02\x00\x00\x00"
            "\x02\x00\x00\x00")));
    EXPECT_EQ(3, x.x.size());
    EXPECT_EQ(2, x.x[0]);
    EXPECT_EQ(2, x.x[1]);
    EXPECT_EQ(2, x.x[2]);
}

TEST(generated_paddings, ArraypadCounterSeparated)
{
    std::vector<char> data(1024);

    ArraypadCounterSeparated x{2, {3}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x02\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x03\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x09\x00\x00\x00"
            "\x02\x00\x00\x00"
            "\x04\x00\x00\x00"
            "\x06\x00\x00\x00")));
    EXPECT_EQ(2, x.x.size());
    EXPECT_EQ(4, x.x[0]);
    EXPECT_EQ(6, x.x[1]);
    EXPECT_EQ(9, x.y);
}

TEST(generated_paddings, ArraypadCounterAligns)
{
    std::vector<char> data(1024);

    ArraypadCounterAligns x{1, {{2}}};
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01" "\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x05" "\xFF\xFF\xFF"
            "\x03\x00\x00\x00"
            "\x02\x03\x04" "\xFF")));
    EXPECT_EQ(5, x.x);
    EXPECT_EQ(3, x.y.x.size());
    EXPECT_EQ(2, x.y.x[0]);
    EXPECT_EQ(3, x.y.x[1]);
    EXPECT_EQ(4, x.y.x[2]);
}

TEST(generated_paddings, ArraypadFixed)
{
    std::vector<char> data(1024);

    ArraypadFixed x{1, prophy::array<uint8_t, 3>{{2, 3, 4}}, 5};
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x02\x03\x04" "\x00"
            "\x05\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x02\x00\x00\x00"
            "\x03\x04\x05" "\x00"
            "\x06\x00\x00\x00")));
    EXPECT_EQ(2, x.x);
    EXPECT_EQ(3, x.y[0]);
    EXPECT_EQ(4, x.y[1]);
    EXPECT_EQ(5, x.y[2]);
    EXPECT_EQ(6, x.z);
}

TEST(generated_paddings, ArraypadDynamic)
{
    std::vector<char> data(1024);

    ArraypadDynamic x{{2}, 3};
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"
            "\x03\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x02\x00\x00\x00"
            "\x02\x03" "\x00\x00"
            "\x02\x00\x00\x00")));
    EXPECT_EQ(2, x.x.size());
    EXPECT_EQ(2, x.x[0]);
    EXPECT_EQ(3, x.x[1]);
    EXPECT_EQ(2, x.y);
}

TEST(generated_paddings, ArraypadLimited)
{
    std::vector<char> data(1024);

    ArraypadLimited x{{2}, 3};
    size_t size = x.encode(data.data());

    EXPECT_EQ(12, size);
    EXPECT_EQ(size, x.get_byte_size());
    EXPECT_EQ(bytes(
            "\x01\x00\x00\x00"
            "\x02" "\x00\x00\x00"
            "\x03\x00\x00\x00"),
            bytes(data.data(), size));

    EXPECT_TRUE(x.decode(bytes(
            "\x02\x00\x00\x00"
            "\x02\x02" "\x00\x00"
            "\x01\x00\x00\x00")));
    EXPECT_EQ(2, x.x.size());
    EXPECT_EQ(2, x.x[0]);
    EXPECT_EQ(2, x.x[1]);
    EXPECT_EQ(1, x.y);
}
