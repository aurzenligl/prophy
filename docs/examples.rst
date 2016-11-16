.. _examples:

Examples
########################

This section tries to present how Prophy language and codecs may be put to work
on an example with moderately complex data structure.

In each tutorial we'll:

  - write a .prophy file,
  - use compiler to generate chosen codec,
  - use this codec to write and read data.

This is the .prophy input file used in all tutorials.
It's sufficiently complex to express various Prophy features.
Let's call it ``values.prophy``:

.. include:: example/values.prophy
    :literal:

Python basics
====================

Compilation
---------------

Prophy Compiler can be used to generate Python codec like this::

    prophyc --python_out . values.prophy

Result is a file, which - together with Prophy Python library - forms a fully functional codec.
It's called ``values.py`` and looks like this:

.. include:: example/values.py
    :literal:

Write and read
------------------

Now we'd need to write a small script to fill Values with some data.
Values can be printed on screen as text, encoded as binary buffer.
On the other communication end, this binary buffer can be used to retrieve the same data:

.. include:: example/python.py
    :literal:

This is what print statement would generate::

    transaction_id: 1234
    objects {
      token {
        id: 0
      }
      updated_values: ''
    }
    objects {
      token {
        keys {
          key_a: 1
          key_b: 2
          key_c: 3
        }
      }
      values: 1
      values: 2
      values: 3
      values: 4
      values: 5
      updated_values: '\x0e'
    }

This is how encoded data looks like::

    d2040000 - transaction id
    02000000 - number of objects

    first, empty object
    00000000   ...
    00000000   ...
    00000000   ...
    00000000   ...
    00000000   ...
    00000000   ...
    00000000   ...
    00000000   ...

    second, filled object
    01000000 - token discriminated as keys
    01000000 - key a
    02000000 - key b
    03000000 - key c
    00000000   ...
    05000000 - number of values
    01000000 - value[0]
    00000000   ...
    02000000 - value[1]
    00000000   ...
    03000000 - value[2]
    00000000   ...
    04000000 - value[3]
    00000000   ...
    05000000 - value[4]
    00000000   ...
    01000000 - length of updated counters
    0e000000 - updated counters

C++ full basics
=====================

Compilation
----------------

Prophy Compiler can be used to generate C++ full codec like this::

    prophyc --cpp_full_out . values.prophy

Result is a pair of header and source files, which - together with Prophy C++ library - form
a fully functional codec. They're called ``values.ppf.hpp`` and ``values.ppf.cpp`` and look like this:

.. literalinclude:: example/values.ppf.hpp
    :language: cpp

.. literalinclude:: example/values.ppf.cpp
    :language: cpp

Write and read
------------------

We can create a program which fills message with data, encodes it,
then decodes buffer to another instance of message and prints it:

.. literalinclude:: example/cpp_full.cpp
    :language: cpp

Program outputs::

    d2040000
    02000000
    00000000
    00000000
    00000000
    00000000
    00000000
    00000000
    00000000
    00000000
    01000000
    01000000
    02000000
    03000000
    00000000
    05000000
    01000000
    00000000
    02000000
    00000000
    03000000
    00000000
    04000000
    00000000
    05000000
    00000000
    01000000
    0e000000
    transaction_id: 1234
    objects {
      token {
        id: 0
      }
      updated_values: ''
    }
    objects {
      token {
        keys {
          key_a: 1
          key_b: 2
          key_c: 3
        }
      }
      values: 1
      values: 2
      values: 3
      values: 4
      values: 5
      updated_values: '\x0e'
    }

C++ raw basics
=====================

Compilation
---------------

Prophy Compiler can be used to generate C++ raw codec like this::

    prophyc --cpp_out . values.prophy

Result is a file, which contains C++ structs with layout intended to be identical to
Prophy wire format. It's ``values.pp.hpp`` and looks like this:

.. literalinclude:: example/values.pp.hpp
    :language: cpp

.. warning ::

   C++ raw codec assumes specific struct padding heuristics
   (natural alignment and special rules for nested dynamic fields)
   and requires enum to be represented as a 32-bit integral value.
   It's tested on gcc, clang and ti cgt on a couple of 32- and 64-bit platforms,
   but your platform ABI may break these rules.

It's accompanied by ``values.pp.cpp`` with endianness swap algorithms for structs and unions:

.. literalinclude:: example/values.pp.cpp
    :language: cpp

Write and read
------------------

We can create a program to write data to buffer and read from it:

.. literalinclude:: example/cpp.cpp
    :language: cpp

This program outputs::

    byte size: 112
    d2040000
    02000000
    00000000
    00000000
    00000000
    00000000
    00000000
    00000000
    00000000
    00000000
    01000000
    01000000
    02000000
    03000000
    00000000
    05000000
    01000000
    00000000
    02000000
    00000000
    03000000
    00000000
    04000000
    00000000
    05000000
    00000000
    01000000
    0e000000
    number of values: 0
    number of values: 5
    value: 1
    value: 2
    value: 3
    value: 4
    value: 5
