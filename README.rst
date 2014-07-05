Prophy
======

``prophy`` is a cross-language, cross-platform data interchange format.
It has compiler and runtime libraries and is similar in purpose to:

- `ASN.1 <http://lionet.info/asn1c/basics.html>`_,
- `Google Protobuf <https://developers.google.com/protocol-buffers/docs/overview>`_,
- `Apache Thrift <http://thrift.apache.org/>`_.

Requirements
------------

- Python 2.7

If you need sack mode in prophyc:
- libclang, at least 3.4
- Python libclang adapter with corresponding version

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

``prophyc`` compiler is meant to process message defition files,
which can be given in different formats, and generate codecs in target language.
Codecs using varying platforms and languages must produce and understand the same data.

.. warning::
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

One format in which ``prophy`` message can be defined is
a mix of C language and patches, called ``sack``.

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
from non-native to native (``test.pp.cpp``):

    template <>
    Test* swap<Test>(Test* payload)
    {
        swap(&payload->num_of_x);
        return cast<Test*>(swap_n_fixed(payload->x, payload->num_of_x));
    }

Isar
----

Another format is xml, called ``isar``.

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

Work remaining
--------------

Prophy is a work in progress.
In order to make it resemble mature frameworks it needs:

- dedicated message definition language as input.
