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

- ``prophy``: dedicated language to express prophy types best
- ``sack``: C++ headers with struct definitions
- ``isar``: xml files

``prophyc`` generates following outputs:

- C++: structs and endianness swapping functions
- Python: full-fledged codecs

Example of compiler usage::

    prophyc --python_out . --cpp_out . my_message.prophy
