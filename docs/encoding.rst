Encoding
####################

This section describes how serialized prophy messages look like.

Prophy message wire format features no field or type tags,
no submessage delimiters and no integer packing.

Prophy ensures that each field in message is aligned.
This allows to manipulate message directly in serialized buffer
and contributes to encoding speed.

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

.. note ::
    All following examples will have numbers encoded
    in little endian for the sake of brevity.

Array
==========

Fixed array
------------

Dynamic array
--------------

Limited array
---------------

Greedy array
--------------

Struct array
===============

A sequence of fields which get serialized in order. Following struct::

    struct X
    {
        u16 x;
        u16 y;
    };

with fields set to 1 and 2 will yield::

    01 00 02 00

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

Dynamic struct
----------------

Dynamic struct padding
-------------------------

Unlimited struct
-------------------

Optional struct field
-------------------------

Union
=================
