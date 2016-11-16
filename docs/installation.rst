Installation
------------

Prophy requires Python 2.7 or Python 3.4 (or newer).
You can install it via `PyPI <https://pypi.python.org/pypi/prophy>`_::

    pip install prophy

If you need :ref:`sack mode<other_schemas_sack>` in Prophy Compiler, you also need:

- libclang, at least 3.4
- Python libclang adapter with corresponding version

In order to compile C++ codecs and dependent code, you'll need to deploy
in your distribution or build system directory with C++ prophy header-only library::

    prophy_cpp/include/prophy

so that includes in generated code are found by compiler::

   #include <prophy/prophy.hpp>

Project is `hosted on github <https://github.com/aurzenligl/prophy>`_.
