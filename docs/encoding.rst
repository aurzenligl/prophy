Encoding
--------

``prophy`` message wire format differs from other toolchains.
There are no field tags, message delimiters and integer packing.

This ``protobuf`` message::

    message Test {
        required int32 x = 1;
    }

with ``x`` set to 150 encodes as::

    08 96 01

while this ``prophy`` message::

    #include <stdint.h>
    struct Test {
        int32_t x;
    };

with ``x`` set to 150 encodes as::

    96 00 00 00

or::

    00 00 00 96

depending on endianness.

``prophy`` ensures that each field in message is aligned.
This allows to manipulate message directly in serialized buffer
and contributes to encoding speed.

``prophy`` supports integers, enums,
arrays (fixed, dynamic and limited) and unions.
