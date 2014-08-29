C++ raw codec
===============

This page describes how to manipulate prophy messages using C++ structs.
This is the fastest option, because structs reflect serialized data format.

.. warning ::

   C++ raw codec assumes specific struct padding heuristics
   and requires enum to be represented as a 32-bit integral value.
   It's tested only with gcc compiler on a number of 32- and 64-bit platforms.

Compilation
----------------

Prophy Compiler can be used to generate C++ raw codec source code from .prophy files.
This generated code together with C++ raw prophy header-only library
forms a fully functional codec.

Example compiler invocation::

    prophyc --cpp_out . test.prophy

will result in creating test.py.

Generated code
----------------

Given following schema::

    //test.prophy
    struct Test
    {
        u32 x<>;
    };

codec can be used this way::

    prophy::Test* msg = static_cast<prophy::Test*>(
        malloc(
            sizeof(prophy::Test) - sizeof(prophy::Test::x)
            + 2 * sizeof(prophy::Test::num_of_x)
        )
    );
    msg.num_of_x = 2;
    msg.x[0] = 1;
    msg.x[1] = 2;
