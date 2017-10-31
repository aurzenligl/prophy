Other schema languages
========================

Prophy Compiler may parse other schemas than the regular one.

Patch
------------

Since other schemas are limited to a subset of Prophy schema features,
they may require `patching` in order to achieve expected form.

Patch file can have patch rules and blank lines.
If message is not found, compilation is still successful.
If message is found but rule does not apply, compilation fails.

If one of rules changes name of node, all rules for original name
still apply, but rules for new name do not apply.

There are following patch rules:

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

  Makes field a fixed array. Only fixed size types can be fixed arrays.

- ``<MESSAGE_NAME> limited <FIELD_NAME> <SIZE_FIELD_NAME>``

  Makes field a limited array, a combination of fixed and dynamic array.
  Field needs to be a fixed array to begin with. Limited array
  may have varying number of elements - up to limit - but it
  always has fixed size.

- ``<MESSAGE_NAME> struct``

  Changes union to struct with fields of respective types.

- ``<NODE_NAME> rename <NODE_NAME>``

  Changes node name.

- ``<MESSAGE_NAME> rename <FIELD_NAME> <NEW_FIELD_NAME>``

  Changes struct or union member name.

.. _other_schemas_sack:

Sack schema
------------

Prophy messages can be defined in a C++ language subset, called Sack.

In this mode Prophy messages are defined by C++ structs and classes,
which may contain enums, typedefs and unions.

With this definition::

    // test.hpp
    #include <stdint.h>
    struct Test {
        uint32_t num_of_x;
        uint32_t x[1];
    };

and this patch::

    //patch.txt
    Test dynamic x num_of_x

this command::

    prophyc --sack --patch patch.txt --python_out . test.hpp

creates a Python codec equivalent to::

    struct Test
    {
        u32 x<>;
    };

Isar schema
------------

This schema is based on xml.

Isar xml may contain definitions of messages, enums, constants,
typedefs and unions.

With this definition::

    // test.xml
    <xml>
        <struct name="Test">
            <member name="x" type="u32">
                <dimension isVariableSize="true"/>
            </member>
        </struct>
    </xml>

this command::

    prophyc --isar --python_out . test.xml

generates identical codec to one from previous example.

Mixing Isar and Sack
--------------------

Since version ``1.1.0`` there is a possibility to implicitly include Isar definitions to
Sack schema compilation. That's useful if the Sack code (c++) depends on many definitions originated in
Isar XMLs. Probably in normal way these are supplied in C++ form by monstrual build system.
This feature allows to skip the 'build system' stage and supplement definitions directly from Isar XMLs.

Having Isar code defining ``Test`` type from previous subchapter (the ``test.xml`` file) you can successfully
compile it with such a Sack code::

   // mixing.hpp
   #include <stdint.h>
   
   struct MixingTest
   {
       int32_t field_a;
       Test field_b;
   };

.. note::

  There is missing definition of ``Test`` and that would fail to compile with any c/c++ compiler. No includes
  are defined, nor exising in filesystem, besides the ``test.xml``. It's up to user to prepare c/c++ file, e.g.
  remove all problematic inclusions (if any). Types from isar doesn't need to be explicitly included in 
  the compiled C/C++ code.

Such a prophyc call::

  prophyc --sack --include_isar test.xml --python_out . mixing.hpp

...will generate two python files.

1. Comming from Isar: ``test.xml`` -> ``test.py``::

    # test.py
    import prophy

    class Test(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('x_len', prophy.u32),
                       ('x', prophy.array(prophy.u32, bound = 'x_len'))]

2. And from the sack code ``mixing.hpp`` -> ``mixing.py``::

    # mixing.py
    import prophy

    from test import *

    class MixingTest(prophy.with_metaclass(prophy.struct_generator, prophy.struct)):
        _descriptor = [('field_a', prophy.i32),
                       ('field_b', Test)]
