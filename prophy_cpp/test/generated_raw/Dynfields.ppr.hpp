#ifndef _PROPHY_GENERATED_RAW_Dynfields_HPP
#define _PROPHY_GENERATED_RAW_Dynfields_HPP

#include <prophy/prophy.hpp>

#include "Arrays.ppr.hpp"

namespace raw
{

struct Dynfields
{
    uint32_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint16_t num_of_y;
        uint16_t y[1];
    } _2;

    struct part3
    {
        uint8_t num_of_z;
        uint64_t z[1];
    } _3;
};

struct DynfieldsMixed
{
    uint32_t num_of_x;
    uint16_t num_of_y;
    uint8_t x[1];

    struct part2
    {
        uint16_t y[1];
    } _2;
};

struct DynfieldsOverlapped
{
    uint32_t num_of_a;
    uint32_t num_of_b;
    uint16_t b[1];

    struct part2
    {
        uint32_t num_of_c;
        uint16_t c[1];
    } _2;

    struct part3
    {
        uint16_t a[1];
    } _3;
};

struct DynfieldsPadded_Helper
{
    uint8_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint32_t num_of_y;
        uint8_t y[1];
    } _2;

    struct part3
    {
        uint64_t z;
    } _3;
};

struct DynfieldsPadded
{
    uint8_t x;
    DynfieldsPadded_Helper y;
};

struct DynfieldsFixtail
{
    uint8_t num_of_x;
    uint8_t x[1];

    struct part2
    {
        uint32_t y;
        uint64_t z;
    } _2;
};

struct DynfieldsComp
{
    BuiltinDynamic x;

    struct part2
    {
        BuiltinDynamic y;
    } _2;

    struct part3
    {
        BuiltinDynamic z;
    } _3;
};

} // namespace raw

#endif  /* _PROPHY_GENERATED_RAW_Dynfields_HPP */
