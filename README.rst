Prophy
======

``prophy`` is a cross-language, cross-platform data interchange format, or protocol.
It has compiler and runtime libraries and is similar in purpose to:

- `XDR <http://tools.ietf.org/html/rfc4506>`_,
- `ASN.1 <http://lionet.info/asn1c/basics.html>`_,
- `Google Protobuf <https://developers.google.com/protocol-buffers/docs/overview>`_,
- `Apache Thrift <http://thrift.apache.org/>`_,
- `Cap'n Proto <http://kentonv.github.io/capnproto/>`_.

Requirements
------------

- Python 2.7

If you need sack mode in prophyc:

- libclang, at least 3.4
- Python libclang adapter with corresponding version

Laguage
--------

Prophy language features following built-in types:

- ``i8``, signed 1-byte integer,
- ``i16``, signed 2-byte integer,
- ``i32``, signed 4-byte integer,
- ``i64``, signed 8-byte integer,
- ``u8``, unsigned 1-byte integer,
- ``u16``, unsigned 2-byte integer,
- ``u32``, unsigned 4-byte integer,
- ``u64``, unsigned 8-byte integer,
- ``float``, 32-bit floating number,
- ``double``, 64-bit floating double-precision number,

Prophy allows to define constants::

    const MY_MIN = -1
    const MY_MAX = 0xFFF

Typedefs::

    typedef u32 my_new_int;

Enums::

    enum MyEnum
    {
        MyEnum_1 = 1,
        MyEnum_2 = 2,
        MyEnum_3 = 3
    }

Structs::

    struct MyStruct
    {
        u32 x;
    };

Structs may contain arrays, which can be:

- fixed: fixed-length::

    struct MyStruct
    {
        u32 x[10];
    };

- dynamic: variable-length::

    struct MyStruct
    {
        u32 x<>;
    };

- limited: variable-length with maximum number of elements and fixed-length on wire::

    struct MyStruct
    {
        u32 x<10>;
    };

- greedy: encoded to wire without delimiter indicating length,
  any struct could contain only one such array as the last field::

    struct MyStruct
    {
        u32 x<...>;
    };

Struct can contain bytes fields, which are byte arrays coming in the same 4 flavors::

    struct MyStruct
    {
        bytes a[10];
        bytes b<>;
        bytes c<10>;
        bytes d<...>;
    };

Struct field can be optional::

    struct MyStruct
    {
        u32* x;
    };

Discriminated unions, which may have hardcoded numbers, constants or enumerators as discriminators::

    union MyUnion
    {
        1: i8 a;
        2: u64 b;
        3: SomeType c;
    };

Currently there are no includes or namespaces in the language.

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

Compiler
--------

``prophyc`` compiler is meant to process message definition files,
which can be given in different formats, and generate codecs in target language.
Codecs using varying platforms and languages must produce and understand the same data.

.. warning ::

   C++ output makes assumptions about compiler's struct padding heuristics,
   and requires enum to be represented as a 32-bit integral value.
   It has been tested with gcc compiler on a number of 32- and 64-bit platforms.

``prophyc`` accepts following inputs:

- ``sack``: C++ headers with struct definitions
- ``isar``: xml files

``prophyc`` generates following outputs:

- C++: structs and endianness swapping functions
- Python: full-fledged codecs

Sack
----

Other format in which ``prophy`` message can be defined is
a mix of C++ language and patches, called ``sack``.

In this mode prophy messages are defined by C++ structs and classes,
which may contain enums, typedefs and unions.

With this definition (``test.hpp``)::

    #include <stdint.h>
    struct Test {
        uint32_t num_of_x;
        uint32_t x[1];
    };

and this patch (``patch.txt``)::

    Test dynamic x num_of_x

this command::

    prophyc --sack --patch patch.txt --python_out . test.hpp

creates a Python codec (``test.py``)::

    import prophy
    class Test(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [('num_of_x', prophy.u32),
                       ('x', prophy.array(prophy.u32, bound = 'num_of_x'))]

which can be used in following way::

    >>> import test
    >>> msg = test.Test()
    >>> msg.x[:] = [1, 2]
    >>> msg.encode('<')
    '\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00'
    >>> print x
    x: 1
    x: 2

C++ codec can be produced via::

    prophyc --sack --patch patch.txt --cpp_out . test.hpp

It consists of hpp file with struct definition (``test.pp.hpp``)::

    struct Test
    {
        uint32_t num_of_x;
        uint32_t x[1]; /// dynamic array, size in num_of_x
    };

and cpp file with function swapping message endianness
from non-native to native (``test.pp.cpp``)::

    template <>
    Test* swap<Test>(Test* payload)
    {
        swap(&payload->num_of_x);
        return cast<Test*>(swap_n_fixed(payload->x, payload->num_of_x));
    }

Isar
----

Yet another format is xml, called ``isar``.

Isar xml may contain definitions of messages, enums, constants,
typedefs and unions.

With this definition (``test.xml``)::

    <xml>
        <struct name="Test">
            <member name="x" type="u32">
                <dimension isVariableSize="true"/>
            </member>
        </struct>
    </xml>

this command::

    prophyc --isar --python_out . --cpp_out . test.xml

generates identical codecs to ones from previous example.

Patch
-----

Patch file may be used to change contents of prophy messages.
This is needed to express all prophy features, which sack and isar
modes are unable to express.

Patch file can have correct instructions and blank lines.
If message is not found, compilation is still successful.
If message is found but instruction does not apply, compilation fails.

There are following patch instructions:

- ``<MESSAGE_NAME> type <FIELD_NAME> <NEW_TYPE>``

  Changes type of message field.

- ``<MESSAGE_NAME> insert <FIELD_INDEX> <FIELD_NAME> <FIELD_TYPE>``

  Inserts a new field in message. Index 0 puts field at the beginning,
  index larger than number of fields, e.g. 999 puts field at the end.
  Newly inserted field is a scalar, not array. Turning it into an array
  requires another instruction.

- ``<MESSAGE_NAME> remove <FIELD_NAME>``

  Removes field from message.

- ``<MESSAGE_NAME> dynamic <FIELD_NAME> <SIZE_FIELD_NAME>``

  Makes field a dynamic array by associating it with a size field.

- ``<MESSAGE_NAME> greedy <FIELD_NAME>``

  Makes field a greedy array. Greedy array doesn't have a size field,
  codecs deduce such array size by parsing message until all bytes are exhausted.
  There can be only one greedy field in any message as last field.

- ``<MESSAGE_NAME> static <FIELD_NAME> <ARRAY_SIZE>``

  Makes field a fixed array. Size needs to be 1 or bigger.
  Only fixed size types can be fixed arrays.

- ``<MESSAGE_NAME> limited <FIELD_NAME> <SIZE_FIELD_NAME>``

  Makes field a limited array, a combination of fixed and dynamic array.
  Field needs to be a fixed array to begin with. Limited array
  may have varying number of elements - up to limit - but it
  always has fixed size.
