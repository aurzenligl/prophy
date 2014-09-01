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

C++ raw basics
=====================

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
        Object objects<>;
    };

Compilation
---------------

Then we'd use Prophy Compiler to generate C++ raw codec for this data structure::

    prophyc --cpp_out . values.prophy

Result is a file, which contains C++ structs with layout intended to be identical to
Prophy wire format. It's ``values.pp.hpp`` and looks like this::

    #ifndef _PROPHY_GENERATED_values_HPP
    #define _PROPHY_GENERATED_values_HPP

    #include <prophy/prophy.hpp>

    struct Keys
    {
        uint32_t key_a;
        uint32_t key_b;
        uint32_t key_c;
    };

    struct Nodes
    {
        uint32_t num_of_nodes;
        uint32_t nodes[3]; /// limited array, size in num_of_nodes
    };

    struct Token
    {
        enum _discriminator
        {
            discriminator_id = 0,
            discriminator_keys = 1,
            discriminator_nodes = 2
        } discriminator;

        union
        {
            uint32_t id;
            Keys keys;
            Nodes nodes;
        };
    };

    struct Object
    {
        Token token;
        uint32_t num_of_values;
        int64_t values[1]; /// dynamic array, size in num_of_values

        struct part2
        {
            uint32_t num_of_updated_values;
            uint8_t updated_values[1]; /// dynamic array, size in num_of_updated_values
        } _2;
    };

    struct Values
    {
        uint32_t transaction_id;
        uint32_t num_of_objects;
        Object objects[1]; /// dynamic array, size in num_of_objects
    };

    #endif  /* _PROPHY_GENERATED_values_HPP */

.. warning ::

   C++ raw codec assumes specific struct padding heuristics
   and requires enum to be represented as a 32-bit integral value.
   It's tested only with gcc compiler on a number of 32- and 64-bit platforms.

It's accompanied by ``values.pp.cpp`` with endianness swap algorithms for structs and unions::

    #include "values.pp.hpp"

    namespace prophy
    {

    template <>
    Keys* swap<Keys>(Keys* payload)
    {
        swap(&payload->key_a);
        swap(&payload->key_b);
        swap(&payload->key_c);
        return payload + 1;
    }

    template <>
    Nodes* swap<Nodes>(Nodes* payload)
    {
        swap(&payload->num_of_nodes);
        swap_n_fixed(payload->nodes, payload->num_of_nodes);
        return payload + 1;
    }

    template <>
    Token* swap<Token>(Token* payload)
    {
        swap(reinterpret_cast<uint32_t*>(&payload->discriminator));
        switch (payload->discriminator)
        {
            case Token::discriminator_id: swap(&payload->id); break;
            case Token::discriminator_keys: swap(&payload->keys); break;
            case Token::discriminator_nodes: swap(&payload->nodes); break;
            default: break;
        }
        return payload + 1;
    }

    inline Object::part2* swap(Object::part2* payload)
    {
        swap(&payload->num_of_updated_values);
        return cast<Object::part2*>(swap_n_fixed(payload->updated_values, payload->num_of_updated_values));
    }

    template <>
    Object* swap<Object>(Object* payload)
    {
        swap(&payload->token);
        swap(&payload->num_of_values);
        Object::part2* part2 = cast<Object::part2*>(swap_n_fixed(payload->values, payload->num_of_values));
        return cast<Object*>(swap(part2));
    }

    template <>
    Values* swap<Values>(Values* payload)
    {
        swap(&payload->transaction_id);
        swap(&payload->num_of_objects);
        return cast<Values*>(swap_n_dynamic(payload->objects, payload->num_of_objects));
    }

    } // namespace prophy

Write and read
------------------

We can create a program to write data to buffer and read from it::

    #include <stdint.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    #include "values.pp.hpp"

    void print_bytes(const void* opaque_data, size_t size)
    {
        const uint8_t* data = static_cast<const uint8_t*>(opaque_data);
        for (int i = 0; i < size; i++)
        {
            if (i && (i % 4 == 0))
            {
                printf("\n");
            }
            printf("%02x", data[i]);
        }
        printf("\n");
    }

    void print_values(Values* x, int index)
    {
        Object* obj = x->objects;
        while(index)
        {
            Object::part2* obj_part2 = prophy::cast<Object::part2*>(
                    obj->values + obj->num_of_values);
            obj = prophy::cast<Object*>(
                    obj_part2->updated_values +
                    obj_part2->num_of_updated_values);
            --index;
        }
        printf("number of values: %d\n", obj->num_of_values);
        for (int i = 0; i < obj->num_of_values; i++)
        {
            printf("value: %d\n", obj->values[i]);
        }
    }

    int main()
    {
        void* data = malloc(1024);
        memset(data, 0, 1024);

        Values* x = static_cast<Values*>(data);
        x->transaction_id = 1234;
        x->num_of_objects = 2;

        Object* obj = x->objects;
        obj->token.discriminator = Token::discriminator_id;
        obj->token.id = 0;
        obj->num_of_values = 0;
        Object::part2* obj_part2 = prophy::cast<Object::part2*>(obj->values);
        obj_part2->num_of_updated_values = 0;

        obj = prophy::cast<Object*>(obj_part2->updated_values);
        obj->token.discriminator = Token::discriminator_keys;
        obj->token.keys.key_a = 1;
        obj->token.keys.key_b = 2;
        obj->token.keys.key_c = 3;
        obj->num_of_values = 5;
        obj->values[0] = 1;
        obj->values[1] = 2;
        obj->values[2] = 3;
        obj->values[3] = 4;
        obj->values[4] = 5;
        obj_part2 = prophy::cast<Object::part2*>(obj->values + 5);
        obj_part2->num_of_updated_values = 1;
        obj_part2->updated_values[0] = 0x0e;

        size_t byte_size =
            reinterpret_cast<uint8_t*>(prophy::cast<Values*>(obj_part2->updated_values + 1)) -
            reinterpret_cast<uint8_t*>(x);

        printf("byte size: %d\n", byte_size);
        print_bytes(x, byte_size);
        print_values(x, 0);
        print_values(x, 1);

        return 0;
    }

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
