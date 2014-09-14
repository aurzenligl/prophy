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
