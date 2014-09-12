#ifndef _PROPHY_GENERATED_Paddings_HPP
#define _PROPHY_GENERATED_Paddings_HPP

#include <stdint.h>
#include <string>
#include <vector>
#include <prophy/endianness.hpp>

struct Endpad
{
    enum { encoded_byte_size = 4 };

    uint16_t x;
    uint8_t y;

    template <prophy::endianness E>
    size_t encode(void* data) const;
    size_t encode(void* data) const { return encode<prophy::native>(data); }
};

//EndpadFixed
//EndpadDynamic
//EndpadLimited
//EndpadGreedy

#endif  /* _PROPHY_GENERATED_Paddings_HPP */
