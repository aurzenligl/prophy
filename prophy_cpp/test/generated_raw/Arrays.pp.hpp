#ifndef _PROPHY_GENERATED_Arrays_HPP
#define _PROPHY_GENERATED_Arrays_HPP

#include <prophy/prophy.hpp>

struct Builtin
{
    uint8_t a;
    uint16_t b;
};

struct BuiltinFixed
{
    uint16_t a[3];
};

struct BuiltinDynamic
{
    uint32_t num_of_x;
    uint16_t x[1]; /// dynamic array, size in num_of_x
};

struct BuiltinLimited
{
    uint32_t num_of_x;
    uint16_t x[3]; /// limited array, size in num_of_x
};

struct BuiltinGreedy
{
    uint16_t x;
    uint32_t y[1]; /// greedy array
};

struct Fixcomp
{
    Builtin a;
    Builtin b;
};

struct FixcompFixed
{
    Builtin a[3];
};

struct FixcompDynamic
{
    uint32_t num_of_x;
    Builtin x[1]; /// dynamic array, size in num_of_x
};

struct FixcompLimited
{
    uint16_t num_of_x;
    Builtin x[3]; /// limited array, size in num_of_x
};

struct FixcompGreedy
{
    uint16_t x;
    Builtin y[1]; /// greedy array
};

struct Dyncomp
{
    BuiltinDynamic x;
};

struct DyncompDynamic
{
    uint32_t num_of_x;
    BuiltinDynamic x[1]; /// dynamic array, size in num_of_x
};

struct DyncompGreedy
{
    uint16_t x;
    BuiltinDynamic y[1]; /// greedy array
};

namespace prophy
{

template <> Builtin* swap<Builtin>(Builtin*);
template <> BuiltinFixed* swap<BuiltinFixed>(BuiltinFixed*);
template <> BuiltinDynamic* swap<BuiltinDynamic>(BuiltinDynamic*);
template <> BuiltinLimited* swap<BuiltinLimited>(BuiltinLimited*);
template <> BuiltinGreedy* swap<BuiltinGreedy>(BuiltinGreedy*);
template <> Fixcomp* swap<Fixcomp>(Fixcomp*);
template <> FixcompFixed* swap<FixcompFixed>(FixcompFixed*);
template <> FixcompDynamic* swap<FixcompDynamic>(FixcompDynamic*);
template <> FixcompLimited* swap<FixcompLimited>(FixcompLimited*);
template <> FixcompGreedy* swap<FixcompGreedy>(FixcompGreedy*);
template <> Dyncomp* swap<Dyncomp>(Dyncomp*);
template <> DyncompDynamic* swap<DyncompDynamic>(DyncompDynamic*);
template <> DyncompGreedy* swap<DyncompGreedy>(DyncompGreedy*);

} // namespace prophy

#endif  /* _PROPHY_GENERATED_Arrays_HPP */
