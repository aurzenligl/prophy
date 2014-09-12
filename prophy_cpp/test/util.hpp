#ifndef _TEST_UTIL_HPP
#define _TEST_UTIL_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/prophy.hpp>

template <class T, size_t N>
void test_swap(const char (&input) [N], const char (&expected) [N], size_t expected_size = N - 1)
{
    std::vector<char> data(input, input + N - 1);
    T* next = prophy::swap(reinterpret_cast<T*>(data.begin().base()));

    EXPECT_EQ(expected_size, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(expected, N - 1), std::string(data.data(), N - 1));
}

static union endianness_finder_t
{
    uint32_t i;
    char c[4];
} endianness_finder = { 0x04030201 };

const bool am_i_little = endianness_finder.c[0] == 1;

struct data
{
    template <size_t N>
    data(const char (&big_) [N], const char (&little_) [N])
        : big(big_, big_ + N - 1),
          little(little_, little_ + N - 1),
          input(am_i_little ? big : little),
          expected(am_i_little ? little : big)
    { }

    std::vector<uint8_t> big;
    std::vector<uint8_t> little;
    std::vector<uint8_t> input;
    std::vector<uint8_t> expected;
};

inline size_t byte_distance(void* first, void* last)
{
    return static_cast<uint8_t*>(last) - static_cast<uint8_t*>(first);
}

#endif  /* _TEST_UTIL_HPP */
