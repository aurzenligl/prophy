.. _encoding:

Encoding
########

This section describes how serialized prophy messages look like.

Prophy message wire format features no field or type tags,
no submessage delimiters and no integer packing.

Prophy ensures that each field in message is aligned.
This allows to manipulate message directly in serialized buffer
and contributes to encoding speed.

There are constraints related to array, struct and union
composability pointed out in this section's notes.

If not stated otherwise all following examples will have numbers
encoded in little endian for the sake of brevity.

.. _encoding_numeric_types:

Numeric types
=============

Prophy encodes integral and floating point numbers according
to their size and endianness. Enums are treated as 32-bit unsigned numbers.

==================  =======================  =======================
Number 42 encodes   as little endian         as big endian
==================  =======================  =======================
u8/i8               2a                       2a
u16/i16             2a 00                    00 2a
u32/i32             2a 00 00 00              00 00 00 2a
u64/i64             2a 00 00 00 00 00 00 00  00 00 00 00 00 00 00 2a
float               00 00 28 42              42 28 00 00
double              00 00 00 00 00 00 45 40  40 45 00 00 00 00 00 00
enum                2a 00 00 00              00 00 00 2a
==================  =======================  =======================

Signed types treat most significant bit as sign bit following U2 encoding rules.

Array
=====

Array is a sequence of elements of the same type.
Elements may be numeric types, structs or unions.

.. note ::
    Dynamic struct may not be held in fixed or limited array.

.. note ::
    Unlimited (greedy) struct may not be held in any array.

There are so much as 5 different types of arrays in Prophy.

Fixed array
-----------

Fixed array has fixed number of elements, hence fixed size on wire. This array::

    u16 x[4];

with elements set to 1, 2, 3 and 4 would encode as::

    01 00 02 00 03 00 04 00

Dynamic array
-------------

Dynamic array has varying number of elements
counted by 32-bit unsigned delimiter. This one::

    u16 x<>;

with 2 elements set to 1 and 2 encodes as::

    02 00 00 00 01 00 02 00

Limited array
-------------

A combination of fixed and dynamic one.
Delimited by an element counter, has fixed size on wire.
This requires it to have an upper limit. Such array::

    u16 x<4>;

with 2 elements set to 1 and 2 encodes as::

    02 00 00 00 01 00 02 00 00 00 00 00

Greedy array
------------

Variable element array without element counter. This one::

    u16 x<...>;

with 2 elements set to 1 and 2 encodes as::

    01 00 02 00

.. note ::
    Greedy array can be used only in the last field of struct.
    Such struct may also be only the last field of any other struct.

Externally sized array
----------------------

An array with externally, explicit defined size::

    u8 size;        // = 2
    u8 x<@size>;    // = [4, 5]
    u16 y<@size>;   // = [6, 7]


with fields set to values from comments above - encodes as::

    02 04 05 00 06 00 07

.. note ::
      - One 'sizer' can describe element quantity of several arrays of different type.
      - The 'sizer' doesn't have to be followed by its sized arrays. There can be anything in between (besides the greedy array).
      - If there are many sized arrays - they can also be splited by other fields.

.. warning ::
    The 'sizer' field needs to be defined:
      - inside the same struct as its sized arrays and
      - placed before these arrays.

    The externally sized array is not supported by :ref:`c++ full<cpp_full>` codec.

Bytes
-----

Bytes field is an array of bytes, which can be handled by codec
in more effective way than an array of u8. Wire format, however,
is the same.

Optional
========

Optional is a fixed-size value prepended by a boolean value encoded as a 32-bit integer.
If it's not set, it's filled with zeroes up to size. This one::

    u32* x;

with x set to 1 would encode as::

    01 00 00 00 01 00 00 00

and with x not set would encode as::

    00 00 00 00 00 00 00 00

.. note ::
    Optional field may not contain unlimited nor dynamic struct.

Struct
======

A sequence of fields which get serialized in strict order. Following struct X::

    struct Nested
    {
        u16 n1;
        u16 n2;
    };

    struct X
    {
        Nested x;
        u32 y;
    };

with fields set to (1, 2) and 3 will yield::

    01 00 02 00 03 00 00 00

Dynamic struct
--------------

Struct containing dynamic arrays directly or indirectly
becomes dynamic itself - its wire representation size varies.

.. note ::
    Dynamic struct may not be held in fixed or limited array.

Unlimited struct
----------------

Struct which contains greedy array or unlimited struct
in the last field becomes an unlimited struct.

.. note ::
    Unlimited struct may not be held in any array or non-last struct field.

Union
=====

Union has fixed size, related to its largest arm size.
It encodes single arm prepended by a field discriminator encoded
as a 32-bit integer. This union::

    struct TwoInts
    {
        u16 a1;
        u16 a2;
    };

    union X
    {
        0: u32 x;
        1: TwoInts y;
    };

with first arm discriminated and set to 1 encodes as::

    00 00 00 00 01 00 00 00

and with second arm discriminated and set to (2, 3) encodes as::

    01 00 00 00 02 00 03 00

.. note ::
    Union arm may not contain unlimited nor dynamic struct, nor array.

.. _encoding_padding:

Padding
=======

Prior examples were deliberately composed of values tiled together without
padding in-between. Facts that:

  - different length integral values are allowed,
  - any field in struct/union (recursively) needs to be aligned to address divisible by its alignment (assuming starting from 0).

makes it necessary to insert padding between struct fields, union discriminator and arm,
optional flag and value, array delimiter and elements or at the end of struct.

Technically padding bytes can have any values, but canonically encoded messages
should be padded with zeroes.

Let's go through a couple of examples.

Integer padding
---------------

In this struct::

    struct
    {
        u8 a;
        u16 b;
    };

field b requires one byte of padding to be aligned::

    01 [00] 02 00

Composite padding
-----------------

Composite (struct or union) alignment is the greatest alignment of its fields.
Optional flag, union discriminator, array delimiter all contribute to struct alignment.
Furthermore - each composite byte-size must be a multiple of its alignment.
In this example struct X::

    struct Nested
    {
        u16 n1;
        u32 n2;
        u16 n3;
    };

    struct X
    {
        u64 x;
        u32 y;
        u8 z;
        Nested n;
    };

illustrates four such paddings:

  #. to align Nested field
  #. to align n2 field
  #. to align Nested struct
  #. to align X struct

::

    01  00  00  00  00  00  00  00
    02  00  00  00  03 [00  00  00]
    04  00 [00  00] 05  00  00  00
    06  00 [00  00][00  00  00  00]

Dynamic array padding
---------------------

Dynamic array is tricky - it requires padding depending on
number of elements. Other than that - usual rules apply.
Such struct::

    struct X
    {
        u8 x<>;
        u8 y<>;
    };

encoded with [1] and [2, 3, 4] will be padded this way::

    01 00 00 00 01 [00 00 00] 03 00 00 00 02 03 04 [00]

if [] and [1, 2, 3, 4] were chosen, there would be no padding at all::

    00 00 00 00 04 00 00 00 01 02 03 04

Arrays with elements exceeding delimiter alignment may require padding::

    struct X
    {
        u64 x<>;
    };

::

    01 00 00 00 [00 00 00 00] 01 00 00 00 00 00 00 00

even if there are no elements (composite padding)::

    00 00 00 00 [00 00 00 00]

Optional padding
----------------

Optional fields don't follow the composite rule, their byte-size
doesn't need to be a multiple of alignment. Thanks to that,
second field in this example doesn't need to be padded
(but struct as such is padded to multiple of 4 - flag alignment)::

    struct X
    {
        u8* x;
        u8 y;
    };

::

    01 00 00 00 01 02 [00 00]

Optional fields can have padding between flag and value,
if value has alignment greater than flag::

    struct X
    {
        u64* x;
    };

::

    01 00 00 00 [00 00 00 00] 01 00 00 00 00 00 00 00

Union padding
-------------

Unions follow composite rule of padding to multiple of alignment::

    union X
    {
        1: u8 x;
    };

::

    01 00 00 00 02 [00 00 00]

and - like optionals - can insert padding between discriminator and arm::

    union X
    {
        1: u64 x;
        2: u8 y;
    };

::

    01 00 00 00 [00 00 00 00] 02 00 00 00 00 00 00 00

Note that:

  - such padding applies to other arms also,
  - shorter arms are padded to largest arm size.

::

    02 00 00 00 [00 00 00 00] 03 [00 00 00 00 00 00 00]

Fields following dynamic fields
-------------------------------

We can split any struct to blocks which end with dynamic fields.
In order to have paddings between non-dynamic fields in blocks
stable regardless of dynamic fields byte-sizes, we need to
propose an unusual rule: first field of such block has the greatest
alignment of all block fields. In other words: block is treated
like composite in that regard::

    struct X
    {
        u8 a<>; // = [1]
        u8 b;   // = 2
        u32 c;  // = 3
        u8 d<>; // = [4]
        u8 e;   // = 5
        u64 f;  // = 6
    };

This one (both arrays set with 1 element only as in comments above) has four paddings:

  #. dynamic padding to align b-d block
  #. to align c field
  #. dynamic padding to align e-f block
  #. to align f field

::

    01  00  00  00  01 [00  00  00]
    02 [00  00  00] 03  00  00  00
    01  00  00  00  04 [00  00  00]
    05 [00  00  00  00  00  00  00]
    06  00  00  00  00  00  00  00
