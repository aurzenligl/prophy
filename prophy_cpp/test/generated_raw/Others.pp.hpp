#ifndef _PROPHY_GENERATED_Others_HPP
#define _PROPHY_GENERATED_Others_HPP

#include <prophy/prophy.hpp>

enum { CONSTANT = 3 };

typedef uint16_t TU16;

enum Enum
{
    Enum_One = 1
};

struct ConstantTypedefEnum
{
    uint16_t a[CONSTANT];
    TU16 b;
    Enum c;
};

struct EnumArrays
{
    Enum a[2];
    uint32_t num_of_b;
    Enum b[2]; /// limited array, size in num_of_b
    uint32_t num_of_c;
    Enum c[1]; /// dynamic array, size in num_of_c
};

struct EnumGreedyArray
{
    Enum x[1]; /// greedy array
};

struct EnumUnion
{
    enum _discriminator
    {
        discriminator_x = 1
    } discriminator;

    union
    {
        Enum x;
    };
};

namespace prophy
{

template <> inline Enum* swap<Enum>(Enum* in) { swap(reinterpret_cast<uint32_t*>(in)); return in + 1; }
template <> ConstantTypedefEnum* swap<ConstantTypedefEnum>(ConstantTypedefEnum*);
template <> EnumArrays* swap<EnumArrays>(EnumArrays*);
template <> EnumGreedyArray* swap<EnumGreedyArray>(EnumGreedyArray*);
template <> EnumUnion* swap<EnumUnion>(EnumUnion*);

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Others_HPP */
