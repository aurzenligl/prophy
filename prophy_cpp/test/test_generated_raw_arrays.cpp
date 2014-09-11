#include <gtest/gtest.h>
#include <gmock/gmock.h>

#include "generated_raw/Arrays.ppr.hpp"

using namespace testing;
using namespace raw;

TEST(generated_raw_arrays, Builtin)
{
    std::string data("\x01\x00\x00\x02", 4);
    Builtin* next = prophy::swap(reinterpret_cast<Builtin*>(data.begin().base()));

    EXPECT_EQ(4, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string("\x01\x00\x02\x00", 4), std::string(data, 0, 4));
}

TEST(generated_raw_arrays, BuiltinFixed)
{
    std::string data(
            "\x00\x02"
            "\x00\x02"
            "\x00\x02", 6);
    BuiltinFixed* next = prophy::swap(reinterpret_cast<BuiltinFixed*>(data.begin().base()));

    EXPECT_EQ(6, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x02\x00"
            "\x02\x00"
            "\x02\x00", 6), std::string(data, 0, 6));
}

TEST(generated_raw_arrays, BuiltinDynamic)
{
    std::string data(
            "\x00\x00\x00\x03"
            "\x00\x05\x00\x06"
            "\x00\x07\xab\xcd", 12);
    BuiltinDynamic* next = prophy::swap(reinterpret_cast<BuiltinDynamic*>(data.begin().base()));

    EXPECT_EQ(12, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00"
            "\x05\x00\x06\x00"
            "\x07\x00\xab\xcd", 12), std::string(data, 0, 12));
}

TEST(generated_raw_arrays, BuiltinLimited)
{
    std::string data(
            "\x00\x00\x00\x02"
            "\x00\x05\x00\x06"
            "\xab\xcd\xef\xba", 12);
    BuiltinLimited* next = prophy::swap(reinterpret_cast<BuiltinLimited*>(data.begin().base()));

    EXPECT_EQ(12, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x02\x00\x00\x00"
            "\x05\x00\x06\x00"
            "\xab\xcd\xef\xba", 12), std::string(data, 0, 12));
}

TEST(generated_raw_arrays, BuiltinGreedy)
{
    std::string data(
            "\x00\x08\xab\xcd"
            "\x00\x00\x00\x01"
            "\x00\x00\x00\x02", 12);
    BuiltinGreedy* next = prophy::swap(reinterpret_cast<BuiltinGreedy*>(data.begin().base()));

    EXPECT_EQ(4, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x08\x00\xab\xcd"
            "\x00\x00\x00\x01"
            "\x00\x00\x00\x02", 12), std::string(data, 0, 12));
}
