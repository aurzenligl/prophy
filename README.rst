``prophy`` is a statically typed, binary, unpacked serialization protocol.

Having this message definition::

    //test.prophy
    struct Test
    {
        u32 x<>;
    };

``prophy`` compiler `prophyc`::

    prophyc --python_out . test.prophy

generates a Python codec::

    #test.py
    import prophy
    class Test(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [('num_of_x', prophy.u32),
                       ('x', prophy.array(prophy.u32, bound = 'num_of_x'))]

which can be used to encode data::

    >>> import test
    >>> msg = test.Test()
    >>> msg.x[:] = [1, 2]
    >>> msg.encode('<')
    '\x02\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00'
    >>> print x
    x: 1
    x: 2
