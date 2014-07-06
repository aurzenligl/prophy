#ifndef _TEST_UTIL_HPP
#define _TEST_UTIL_HPP

#include <stdint.h>
#include <vector>

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
