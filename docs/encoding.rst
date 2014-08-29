Encoding
--------

Prophy message wire format features no field tags,
no message delimiters and no integer packing.

This Prophy message::

    struct Test
    {
        i32 x;
    };

with x set to 150 encodes as::

    96 00 00 00

or::

    00 00 00 96

depending on endianness.

Prophy ensures that each field in message is aligned.
This allows to manipulate message directly in serialized buffer
and contributes to encoding speed.

Prophy supports integers, enums,
arrays (fixed, dynamic and limited) and unions.
