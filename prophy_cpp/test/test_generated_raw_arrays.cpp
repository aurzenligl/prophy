#include <gtest/gtest.h>

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

TEST(generated_raw_arrays, Fixcomp)
{
    std::string data(
            "\x01\x00\x00\x02"
            "\x01\x00\x00\x02", 8);
    Fixcomp* next = prophy::swap(reinterpret_cast<Fixcomp*>(data.begin().base()));

    EXPECT_EQ(8, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x01\x00\x02\x00"
            "\x01\x00\x02\x00", 8), std::string(data, 0, 8));
}

TEST(generated_raw_arrays, FixcompFixed)
{
    std::string data(
            "\x01\x00\x00\x02"
            "\x01\x00\x00\x02"
            "\x01\x00\x00\x02", 12);
    FixcompFixed* next = prophy::swap(reinterpret_cast<FixcompFixed*>(data.begin().base()));

    EXPECT_EQ(12, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x01\x00\x02\x00"
            "\x01\x00\x02\x00"
            "\x01\x00\x02\x00", 12), std::string(data, 0, 12));
}

TEST(generated_raw_arrays, FixcompDynamic)
{
    std::string data(
            "\x00\x00\x00\x03"
            "\x01\x00\x00\x01"
            "\x02\x00\x00\x02"
            "\x03\x00\x00\x03", 16);
    FixcompDynamic* next = prophy::swap(reinterpret_cast<FixcompDynamic*>(data.begin().base()));

    EXPECT_EQ(16, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00"
            "\x01\x00\x01\x00"
            "\x02\x00\x02\x00"
            "\x03\x00\x03\x00", 16), std::string(data, 0, 16));
}

TEST(generated_raw_arrays, FixcompLimited)
{
    std::string data(
            "\x00\x02"
            "\x01\x00\x00\x01"
            "\x02\x00\x00\x02"
            "\xab\xcd\xef\xba", 14);
    FixcompLimited* next = prophy::swap(reinterpret_cast<FixcompLimited*>(data.begin().base()));

    EXPECT_EQ(14, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x02\x00"
            "\x01\x00\x01\x00"
            "\x02\x00\x02\x00"
            "\xab\xcd\xef\xba", 14), std::string(data, 0, 14));
}

TEST(generated_raw_arrays, FixcompGreedy)
{
    std::string data(
            "\x00\x01"
            "\x01\x00\x00\x01"
            "\x02\x00\x00\x02"
            "\x01\x00\x00\x01"
            "\x02\x00\x00\x02", 18);
    FixcompGreedy* next = prophy::swap(reinterpret_cast<FixcompGreedy*>(data.begin().base()));

    EXPECT_EQ(2, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x01\x00"
            "\x01\x00\x00\x01"
            "\x02\x00\x00\x02"
            "\x01\x00\x00\x01"
            "\x02\x00\x00\x02", 18), std::string(data, 0, 18));
}

TEST(generated_raw_arrays, Dyncomp)
{
    std::string data(
            "\x00\x00\x00\x03"
            "\x00\x01\x00\x02"
            "\x00\x03\xab\xcd", 12);
    Dyncomp* next = prophy::swap(reinterpret_cast<Dyncomp*>(data.begin().base()));

    EXPECT_EQ(12, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x03\x00\x00\x00"
            "\x01\x00\x02\x00"
            "\x03\x00\xab\xcd", 12), std::string(data, 0, 12));
}

TEST(generated_raw_arrays, DyncompDynamic)
{
    std::string data(
            "\x00\x00\x00\x02"
            "\x00\x00\x00\x01"
            "\x00\x01\xef\xab"
            "\x00\x00\x00\x03"
            "\x00\x01\x00\x02"
            "\x00\x03\xab\xcd", 24);
    DyncompDynamic* next = prophy::swap(reinterpret_cast<DyncompDynamic*>(data.begin().base()));

    EXPECT_EQ(24, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x02\x00\x00\x00"
            "\x01\x00\x00\x00"
            "\x01\x00\xef\xab"
            "\x03\x00\x00\x00"
            "\x01\x00\x02\x00"
            "\x03\x00\xab\xcd", 24), std::string(data, 0, 24));
}

TEST(generated_raw_arrays, DyncompGreedy)
{
    std::string data(
            "\x00\x01\xab\xcd"
            "\x00\x00\x00\x01"
            "\x00\x01\xef\xab"
            "\x00\x00\x00\x03"
            "\x00\x01\x00\x02"
            "\x00\x03\xab\xcd", 24);
    DyncompGreedy* next = prophy::swap(reinterpret_cast<DyncompGreedy*>(data.begin().base()));

    EXPECT_EQ(4, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(
            "\x01\x00\xab\xcd"
            "\x00\x00\x00\x01"
            "\x00\x01\xef\xab"
            "\x00\x00\x00\x03"
            "\x00\x01\x00\x02"
            "\x00\x03\xab\xcd", 24), std::string(data, 0, 24));
}
