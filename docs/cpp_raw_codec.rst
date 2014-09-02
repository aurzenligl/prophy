.. _cpp_raw:

C++ raw codec
===============

This page describes how to manipulate prophy messages using C++ structs.
This is the fastest option, because structs reflect serialized data format.
It's also most environment-tolerant, since it reduces necessary operations
to memory reads and writes, and pointer arithmetics.

.. warning ::

   C++ raw codec assumes specific struct padding heuristics
   and requires enum to be represented as a 32-bit integral value.
   It's tested only with gcc compiler on a number of 32- and 64-bit platforms.

Compilation
----------------

Prophy Compiler can be used to generate C++ raw codec source code from .prophy files.
This generated code together with C++ raw prophy header-only library can be used
to write and read Prophy messages.

Example compiler invocation::

    prophyc --cpp_out . test.prophy

will result in creating ``test.pp.hpp`` and ``test.pp.cpp``.
Header file contains struct definitions.
Implementation file contains endianness swap algorithms for structs and unions.

Generated code
----------------

Enums are represented as regular C++ enums::

    enum Test1
    {
        Test1_1 = 1,
        Test1_2 = 2,
        Test1_3 = 3
    };

::

    enum Test1
    {
        Test1_1 = 1,
        Test1_2 = 2,
        Test1_3 = 3
    };

Structs are also represented as regular structs::

    struct Test2
    {
        u32 a;
    };

::

    struct Test2
    {
        uint32_t a;
    };

Arrays are represented as optional element counter and C++ array
depending on type:

  - fixed: C++ arrays,
  - dynamic: uint32_t element counter followed by
    a 1-size C++ array representing variable length array,
  - limited: uint32_t element counter followed by a C++ array,
  - greedy: 1-size C++ array representing variable length array.

::

    struct Test8
    {
        i32 a[3];
        i32 b<>;
        i32 c<3>;
        i32 d<...>;
    };

::

    struct Test8
    {
        int32_t a[3];
        uint32_t num_of_b;
        int32_t b[1]; /// dynamic array, size in num_of_b

        struct part2
        {
            uint32_t num_of_c;
            int32_t c[3]; /// limited array, size in num_of_c
            int32_t d[1]; /// greedy array
        } _2;
    };

Above snippet shows how Prophy handles multiple dynamic fields in single struct:
it defines inner structs with remaining fields.
Field _2 is not meant to be written, it's there merely to get the main struct alignment right.

Optional struct fields are represented by uint32_t alias indicating value presence,
and value itself. Fact that optional field type may not be dynamic simplifies things::

    struct Test6
    {
        u32* a;
        Test2* b;
    };

::

    struct Test6
    {
        prophy::bool_t has_a;
        uint32_t a;
        prophy::bool_t has_b;
        Test2 b;
    };

Union representation is similar to optional field, with
discriminator in place of presence indicator. Union arms
are accessible as members of unnamed inner union::

    union Test7
    {
        0: u32 a;
        1: Test2 b;
    };

::

    struct Test7
    {
        enum _discriminator
        {
            discriminator_a = 0,
            discriminator_b = 1
        } discriminator;

        union
        {
            uint32_t a;
            Test2 b;
        };
    };

How to size message?
-----------------------

Codec lacks support for sizing now. You need to be creative.
You have a couple of options:

  - you can allocate buffer large enough to hold any of your messages,
    write message and see where you are,

  - you can also calculate exact size using sizeof operator,
    but need to be :ref:`careful with padding<encoding_struct_padding>`::

      struct X
      {
          uint32_t num_of_x;
          uint32_t x[1]; /// dynamic array, size in num_of_x
      };

      /// assuming you want to write 5 elements
      size_t msg_size = sizeof(X) - sizeof(uint32_t) + 5 * sizeof(uint32_t);

How to get past dynamic fields?
-------------------------------------

You'll want to use ``prophy::cast`` function to get a pointer
of next field's type, aligned to that type.
Othwerise you'll have problems either with alignment or fulfilling
:ref:`wire format expectations<encoding_dynamic_struct>`::

    struct X
    {
        u32 a<>;
        u32 b<>;
    };

::

    struct X
    {
        uint32_t num_of_a;
        uint32_t a[1]; /// dynamic array, size in num_of_a

        struct part2
        {
            uint32_t num_of_b;
            uint32_t b[1]; /// dynamic array, size in num_of_b
        } _2;
    };

::

    X* x = static_cast<X*>(malloc(1024));
    x->num_of_a = 3;
    x->a[0] = 1;
    x->a[1] = 2;
    x->a[2] = 3;
    X::part2* xp2 = prophy::cast<X::part2*>(x->a + 3);
    xp2->num_of_b = 2;
    xp2->b[0] = 4;
    xp2->b[1] = 5;

How to swap message endianness?
-----------------------------------

Problem exists e.g. when you try to read message encoded on big endian system
on little endian system. It won't work without swapping
:ref:`multi-byte numeric values<encoding_numeric_types>`.

This is what the implementation file and ``prophy::swap`` function are for::

    EndiannessSensitive* msg = ...
    prophy::swap(msg);

If you don't need endianness swapping in your application,
disregard the implementation file altogether.
