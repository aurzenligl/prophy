.. _python:

Python codec
===============

This page describes how to encode, decode and manipulate prophy messages in Python.

Compilation
----------------

Prophy Compiler can be used to generate Python codec source code from .prophy files.
This generated code together with Python prophy library forms a fully functional codec.

Example compiler invocation::

    prophyc --python_out . test.prophy

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

    >>> import test
    >>> msg = test.Test()
    >>> msg.x[:] = [1, 2]
    >>> msg.encode('<')
    '\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00'
    >>> print x
    x: 1
    x: 2

Packed mode
----------------

Python generated message descriptors may be altered
to inhibit padding by inheriting from ``struct_packed`` instead of ``struct``.
Following message would be encoded as 6 bytes::

    class PackedMessage(prophy.struct_packed):
        __metaclass__ = prophy.struct_generator
        _descriptor = [('x', prophy.u8),
                       ('y', prophy.u32),
                       ('z', prophy.u8)]

.. warning::
    Mixing ``struct_packed`` with nested ``struct`` and otherwise yields undefined behavior.
