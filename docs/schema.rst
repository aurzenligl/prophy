.. _schema:

Schema language
====================

Prophy messages are meant to be held in .prophy files.
These files contain structs and unions composed with numeric types,
constants, enums, arrays and nested structs and unions.
All these primitives are explained below.

:ref:`Encoding section <encoding>` explains wire representation of these language constructs.

There are constraints on constructs composability, pointed out in notes.

Numeric types
-------------------

Prophy has following numeric types:

======  ==========================================
i8      signed 8-bit integer
i16     signed 16-bit integer
i32     signed 32-bit integer
i64     signed 64-bit integer
u8      unsigned 8-bit integer
u16     unsigned 16-bit integer
u32     unsigned 32-bit integer
u64     unsigned 64-bit integer
float   32-bit floating single-precision number
double  64-bit floating double-precision number
======  ==========================================

Constant
-----------

Constants for use as array lengths or union discriminators may be defined this way::

    const MY_MIN = -1
    const MY_MAX = 0xFFF

Signed, unsigned decimal, octal and hexal numbers are allowed,
but arithmetic expressions are not.

Enum
---------

Enumerations may be defined in following manner::

    enum MyEnum
    {
        MyEnum_1 = 1,
        MyEnum_2 = 2,
        MyEnum_3 = 3
    };

Enumerators may contain references to other enums or constants,
but arithmetic expressions are forbidden.

Typedef
--------------

Typedef is an alias for previously defined type.
Numeric type, enum, struct, union or other typedef may be aliased::

    typedef u32 my_aliased_int;
    typedef X my_aliased_x;

Struct
----------------

Struct contains fields. Fields can be numeric types, enums,
structs, unions, typedefs or arrays of any former.
There are 4 kinds of arrays:

========   ==================  ======================  =============================
kind       schema              fixed-length on wire    variable number of elements
========   ==================  ======================  =============================
fixed      ``Type x[Size]``    yes                     no
dynamic    ``Type x<>``        no                      yes
limited    ``Type x<Limit>``   yes                     yes (up to limit)
greedy     ``Type x<...>``     no                      yes
========   ==================  ======================  =============================

.. note::
    Fixed and limited array cannot hold dynamic nor unlimited struct.

.. note::
    Greedy array may only be used in the last field of struct.

This is how they can be used in a struct::

    struct X
    {
        u32 a;
        MyUserDefinedType b;
        u32 c[3]; // fixed array of length 3
        u32 d<>; // dynamic array
        u32 e<3>; // limited array of limit 3
        u32 f<...>; // greedy array
    };

Field may be declared as bytes field, if it's meant to hold opaque binary data.
Codec may use this information to manipulate its data in more effective manner.
Same rules as with arrays apply::

    struct X
    {
        bytes a[3];
        bytes b<>;
        bytes c<3>;
        bytes d<...>;
    };

Field may be optional::

    struct X
    {
        u32* x;
    };

.. note::
    Optional field cannot hold dynamic nor unlimited struct.
    There's no optional array.

Union
----------

Discriminated unions are defined like structs, but with
unsigned discriminators at the beginning of each field::

    union MyUnion
    {
        1: i8 a;
        2: u64 b;
        3: SomeType c;
    };

Discriminators may be literals or references to constants or enumerators.

.. note::
    Union arm cannot hold dynamic nor unlimited struct, nor array.

Limitations
-------------

Currently there are no includes or scoped definitions in the language.

American scientists, however, do work on both.
