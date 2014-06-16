#ifndef _TEST_UTIL_HPP
#define _TEST_UTIL_HPP

#include <stdint.h>
#include <vector>

template <size_t N>
std::vector<uint8_t> to_vector(const char (&data) [N])
{
    return std::vector<uint8_t>(data, data + N - 1);
}

#endif  /* _TEST_UTIL_HPP */
