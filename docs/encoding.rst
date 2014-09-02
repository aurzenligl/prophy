.. _encoding:

Encoding
####################

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
====================

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
==========

Array is a sequence of elements of the same type.
Elements may be numeric types, structs or unions.

.. note ::
    Dynamic struct may not be held in fixed or limited array.

.. note ::
    Unlimited struct may not be held in any array.

There are so much as 4 different types of arrays in Prophy.

Fixed array
------------

Fixed array has fixed number of elements, hence fixed size on wire. This array::

    u16 x[4];

with elements set to 1, 2, 3 and 4 would encode as::

    01 00 02 00 03 00 04 00

Dynamic array
--------------

Dynamic array has varying number of elements
counted by 32-bit unsigned delimiter. This one::

    u16 x<>;

with 2 elements set to 1 and 2 encodes as::

    02 00 00 00 01 00 02 00

Limited array
---------------

A combination of fixed and dynamic one.
Delimited by an element counter, has fixed size on wire.
This requires it to have an upper limit. Such array::

    u16 x<4>;

with 2 elements set to 1 and 2 encodes as::

    02 00 00 00 01 00 02 00 00 00 00 00

Greedy array
--------------

Variable element array without element counter. This one::

    u16 x<...>;

with 2 elements set to 1 and 2 encodes as::

    01 00 02 00

.. note ::
    Greedy array can be used only in the last field of struct.
    Such struct may also be only the last field of any other struct.

Bytes
---------

Bytes field is an array of bytes, which can be handled by codec
in more effective way than an array of u8. Wire format, however,
is the same.

Struct
============

A sequence of fields which get serialized in order. Following struct::

    struct X
    {
        u16 x;
        u16 y;
    };

with fields set to 1 and 2 will yield::

    01 00 02 00

.. _encoding_struct_padding:

Struct padding
-----------------

Prophy appends padding after each field if needed to ensure field alignment.
Additionally, last field is padded to fulfil struct alignment. This struct::

    struct X
    {
        u8 x;
        u32 y;
        u16 z;
    };

with fields set to 1, 2 and 3 will have padding denoted by brackets::

    01 [00 00 00] 02 00 00 00 03 00 [00 00]

Nested struct
-----------------

Structs may be nested to express data in hierarchy.
Padding rules apply as if nested struct field was numeric field
with alignment equal to its largest field alignment.
Following structs::

    struct Nested
    {
        u8 a;
        u16 b;
        u8 c;
    };

    struct X
    {
        u8 x;
        Nested y;
        u8 z;
    };

with fields set to 1, (2, 3, 4) and 5 encodes as::

    01 [00] 02 [00] 03 00 04 [00] 05 [00]

.. _encoding_dynamic_struct:

Dynamic struct
----------------

Struct which contains dynamic arrays directly or indirectly
becomes dynamic itself - its wire representation size varies.

It also means its dynamic arrays padding is related to
number of their elements. Example illustrates::

    struct X
    {
        bytes x<>;
        bytes y<>;
    };

with fields set to (1,) and (1, 2, 3) would give::

    01 00 00 00 01 [00 00 00] 03 00 00 00 01 02 03 [00]

.. note ::
    Dynamic struct may not be held in fixed or limited array.

Unlimited struct
-------------------

Struct which contains greedy array or unlimited struct
in the last field becomes an unlimited struct.

.. note ::
    Unlimited struct may not be held in any array.

Optional field
------------------

Optional struct field has fixed size on wire.
It's prepended by a boolean value encoded as a 32-bit integer.
If field is not set, it's filled with zeroes up to size. This one::

    struct X
    {
        u16* x;
    };

with field set to 1 would encode as::

    01 00 00 00 01 00 00 00

and with field not set would encode as::

    00 00 00 00 00 00 00 00

.. note ::
    Optional field may not contain unlimited nor dynamic struct.

Union
=================

Union has fixed size, related to its largest arm size.
It encodes single arm prepended by a field discriminator encoded
as a 32-bit integer. This union::

    union X
    {
        0: u8 x;
        1: u16 y;
    };

with first arm discriminated and set to 1 encodes as::

    00 00 00 00 01 [00 00 00]

and with second arm discriminated and set to 2 encodes as::

    01 00 00 00 02 00 [00 00]

.. note ::
    Union arm may not contain unlimited nor dynamic struct, nor array.