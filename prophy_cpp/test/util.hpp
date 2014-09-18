#ifndef _TEST_UTIL_HPP
#define _TEST_UTIL_HPP

#include <stdint.h>
#include <vector>
#include <prophy/prophy.hpp>

template <size_t N>
std::vector<uint8_t> bytes(const char (&x) [N])
{
    return std::vector<uint8_t>(x, x + N - 1);
}

inline std::vector<uint8_t> bytes(const void* x, size_t size)
{
    return std::vector<uint8_t>(static_cast<const uint8_t*>(x), static_cast<const uint8_t*>(x) + size);
}

template <class T, size_t N>
void test_swap(const char (&input) [N], const char (&expected) [N], size_t expected_size = N - 1)
{
    std::vector<char> data(input, input + N - 1);
    T* next = prophy::swap(reinterpret_cast<T*>(data.begin().base()));

    EXPECT_EQ(expected_size, reinterpret_cast<char*>(next) - data.data());
    EXPECT_EQ(std::string(expected, N - 1), std::string(data.data(), N - 1));
}

#endif  /* _TEST_UTIL_HPP */
