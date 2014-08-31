.. _examples:

Examples
########################

This section tries to present how prophy language and codecs may be put to work
on a moderately complex data structure example.

Python basics
====================

In this tutorial we'll do following things:

  - write a simple .prophy file,
  - use compiler to generate Python codec,
  - use this codec to write and read data.

Prophy file
---------------

First we need to define schema of interesting data structure.
Let's make it sufficiently complex to express various Prophy features
and call it ``values.prophy``::

    struct Keys
    {
        u32 key_a;
        u32 key_b;
        u32 key_c;
    };

    struct Nodes
    {
        u32 nodes<3>;
    };

    union Token
    {
        0: u32 id;
        1: Keys keys;
        2: Nodes nodes;
    };

    struct Object
    {
        Token token;
        i64 values<>;
        bytes updated_values<>;
    };

    struct Values
    {
        u32 transaction_id;
        u64* timestamp;
        Object objects<>;
    };

Compilation
---------------

Then we'd use Prophy Compiler to generate Python codec for this data structure::

    prophyc --python_out . values.prophy

Result is a file, which - together with Prophy Python library - forms a fully functional codec.
It's called ``values.py`` and looks like this::

    import prophy

    class Keys(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [('key_a', prophy.u32),
                       ('key_b', prophy.u32),
                       ('key_c', prophy.u32)]

    class Nodes(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [('num_of_nodes', prophy.u32),
                       ('nodes', prophy.array(prophy.u32, bound = 'num_of_nodes', size = 3))]

    class Token(prophy.union):
        __metaclass__ = prophy.union_generator
        _descriptor = [('id', prophy.u32, 0),
                       ('keys', Keys, 1),
                       ('nodes', Nodes, 2)]

    class Object(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [('token', Token),
                       ('num_of_values', prophy.u32),
                       ('values', prophy.array(prophy.i64, bound = 'num_of_values')),
                       ('num_of_updated_values', prophy.u32),
                       ('updated_values', prophy.bytes(bound = 'num_of_updated_values'))]

    class Values(prophy.struct):
        __metaclass__ = prophy.struct_generator
        _descriptor = [('transaction_id', prophy.u32),
                       ('timestamp', prophy.optional(prophy.u64)),
                       ('num_of_objects', prophy.u32),
                       ('objects', prophy.array(Object, bound = 'num_of_objects'))]

Write and read
------------------

Now we'd need to write a small script to fill Values with some data::

    import values

    x = values.Values()
    x.transaction_id = 1234

    empty_obj = x.objects.add()

    obj = x.objects.add()
    obj.token.discriminator = 'keys'
    obj.token.keys.key_a = 1
    obj.token.keys.key_b = 2
    obj.token.keys.key_c = 3
    obj.values[:] = [1, 2, 3, 4, 5]
    obj.updated_values = '\x0e'

Values could now be printed on screen as text, encoded as binary buffer.
On the other communication end, this binary buffer can be used to retrieve the same data::

    # human readable representation of data
    print x

    # this is how data can be encoded
    data = x.encode('>')

    # this is how data can be decoded
    x.decode(data, '>')

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

    000004d2 - transaction id
    00000000 - non-set timestamp
    00000000   ...
    00000000   ...
    00000000   ...
    00000002 - number of objects

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
    00000001 - token discriminated as keys
    00000001 - key a
    00000002 - key b
    00000003 - key c
    00000000   ...
    00000005 - number of values
    00000000 - value[0]
    00000001   ...
    00000000 - value[1]
    00000002   ...
    00000000 - value[2]
    00000003   ...
    00000000 - value[3]
    00000004   ...
    00000000 - value[4]
    00000005   ...
    00000001 - length of updated counters
    0e000000 - updated counters

C++ raw basics
=====================

Example in construction.
