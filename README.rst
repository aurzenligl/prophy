Prophy is a statically typed, binary, tag-free, unpacked serialization protocol.

You can define message schema::

    //test.prophy
    struct Test
    {
        u16 x<>;
    };

generate codec for chosen language::

    prophyc --python_out . test.prophy

and serialize data::

    >>> import test
    >>> msg = test.Test()
    >>> msg.x[:] = [1, 2, 3, 4]
    >>> msg.encode('<')
    '\x04\x00\x00\x00\x01\x00\x02\x00\x03\x00\x04\x00'

Documentation: http://prophy.readthedocs.org

Issues: https://github.com/aurzenligl/prophy/issues
