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

template <size_t N>
std::vector<uint8_t> to_vector(const char (&data) [N])
{
    return std::vector<uint8_t>(data, data + N - 1);
}

inline size_t byte_distance(void* first, void* last)
{
    return static_cast<uint8_t*>(last) - static_cast<uint8_t*>(first);
}

#endif  /* _TEST_UTIL_HPP */
