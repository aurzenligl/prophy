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
Let's call it ``values.prophy``::

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

Python basics
====================

Compilation
---------------

Prophy Compiler can be used to generate Python codec like this::

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

C++ full basics
=====================

Compilation
----------------

Prophy Compiler can be used to generate C++ full codec like this::

    prophyc --cpp_full_out . values.prophy

Result is a pair of header and source files, which - together with Prophy C++ library - form
a fully functional codec. They're called ``values.ppf.hpp`` and ``values.ppf.cpp`` and look like this::

    #ifndef _PROPHY_GENERATED_FULL_values_HPP
    #define _PROPHY_GENERATED_FULL_values_HPP

    #include <stdint.h>
    #include <numeric>
    #include <vector>
    #include <string>
    #include <prophy/array.hpp>
    #include <prophy/endianness.hpp>
    #include <prophy/optional.hpp>
    #include <prophy/detail/byte_size.hpp>
    #include <prophy/detail/message.hpp>
    #include <prophy/detail/mpl.hpp>

    namespace prophy
    {
    namespace generated
    {

    struct Keys : public prophy::detail::message<Keys>
    {
        enum { encoded_byte_size = 12 };

        uint32_t key_a;
        uint32_t key_b;
        uint32_t key_c;

        Keys(): key_a(), key_b(), key_c() { }
        Keys(uint32_t _1, uint32_t _2, uint32_t _3): key_a(_1), key_b(_2), key_c(_3) { }

        size_t get_byte_size() const
        {
            return 12;
        }
    };

    struct Nodes : public prophy::detail::message<Nodes>
    {
        enum { encoded_byte_size = 16 };

        std::vector<uint32_t> nodes; /// limit 3

        Nodes() { }
        Nodes(const std::vector<uint32_t>& _1): nodes(_1) { }

        size_t get_byte_size() const
        {
            return 16;
        }
    };

    struct Token : public prophy::detail::message<Token>
    {
        enum { encoded_byte_size = 20 };

        enum _discriminator
        {
            discriminator_id = 0,
            discriminator_keys = 1,
            discriminator_nodes = 2
        } discriminator;

        static const prophy::detail::int2type<discriminator_id> discriminator_id_t;
        static const prophy::detail::int2type<discriminator_keys> discriminator_keys_t;
        static const prophy::detail::int2type<discriminator_nodes> discriminator_nodes_t;

        uint32_t id;
        Keys keys;
        Nodes nodes;

        Token(): discriminator(discriminator_id), id() { }
        Token(prophy::detail::int2type<discriminator_id>, uint32_t _1): discriminator(discriminator_id), id(_1) { }
        Token(prophy::detail::int2type<discriminator_keys>, const Keys& _1): discriminator(discriminator_keys), keys(_1) { }
        Token(prophy::detail::int2type<discriminator_nodes>, const Nodes& _1): discriminator(discriminator_nodes), nodes(_1) { }

        size_t get_byte_size() const
        {
            return 20;
        }
    };

    struct Object : public prophy::detail::message<Object>
    {
        enum { encoded_byte_size = -1 };

        Token token;
        std::vector<int64_t> values;
        std::vector<uint8_t> updated_values;

        Object() { }
        Object(const Token& _1, const std::vector<int64_t>& _2, const std::vector<uint8_t>& _3): token(_1), values(_2), updated_values(_3) { }

        size_t get_byte_size() const
        {
            return prophy::detail::nearest<8>(
                values.size() * 8 + updated_values.size() * 1 + 28
            );
        }
    };

    struct Values : public prophy::detail::message<Values>
    {
        enum { encoded_byte_size = -1 };

        uint32_t transaction_id;
        std::vector<Object> objects;

        Values(): transaction_id() { }
        Values(uint32_t _1, const std::vector<Object>& _2): transaction_id(_1), objects(_2) { }

        size_t get_byte_size() const
        {
            return std::accumulate(objects.begin(), objects.end(), size_t(), prophy::detail::byte_size()) + 8;
        }
    };

    } // namespace generated
    } // namespace prophy

    #endif  /* _PROPHY_GENERATED_FULL_values_HPP */

::

    #include "values.ppf.hpp"
    #include <algorithm>
    #include <prophy/detail/encoder.hpp>
    #include <prophy/detail/decoder.hpp>
    #include <prophy/detail/printer.hpp>
    #include <prophy/detail/align.hpp>

    using namespace prophy::generated;

    namespace prophy
    {
    namespace detail
    {

    template <>
    template <endianness E>
    uint8_t* message_impl<Keys>::encode(const Keys& x, uint8_t* pos)
    {
        pos = do_encode<E>(pos, x.key_a);
        pos = do_encode<E>(pos, x.key_b);
        pos = do_encode<E>(pos, x.key_c);
        return pos;
    }
    template uint8_t* message_impl<Keys>::encode<native>(const Keys& x, uint8_t* pos);
    template uint8_t* message_impl<Keys>::encode<little>(const Keys& x, uint8_t* pos);
    template uint8_t* message_impl<Keys>::encode<big>(const Keys& x, uint8_t* pos);

    template <>
    template <endianness E>
    bool message_impl<Keys>::decode(Keys& x, const uint8_t*& pos, const uint8_t* end)
    {
        return (
            do_decode<E>(x.key_a, pos, end) &&
            do_decode<E>(x.key_b, pos, end) &&
            do_decode<E>(x.key_c, pos, end)
        );
    }
    template bool message_impl<Keys>::decode<native>(Keys& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Keys>::decode<little>(Keys& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Keys>::decode<big>(Keys& x, const uint8_t*& pos, const uint8_t* end);

    template <>
    void message_impl<Keys>::print(const Keys& x, std::ostream& out, size_t indent)
    {
        do_print(out, indent, "key_a", x.key_a);
        do_print(out, indent, "key_b", x.key_b);
        do_print(out, indent, "key_c", x.key_c);
    }
    template void message_impl<Keys>::print(const Keys& x, std::ostream& out, size_t indent);

    template <>
    template <endianness E>
    uint8_t* message_impl<Nodes>::encode(const Nodes& x, uint8_t* pos)
    {
        pos = do_encode<E>(pos, uint32_t(std::min(x.nodes.size(), size_t(3))));
        do_encode<E>(pos, x.nodes.data(), uint32_t(std::min(x.nodes.size(), size_t(3))));
        pos = pos + 12;
        return pos;
    }
    template uint8_t* message_impl<Nodes>::encode<native>(const Nodes& x, uint8_t* pos);
    template uint8_t* message_impl<Nodes>::encode<little>(const Nodes& x, uint8_t* pos);
    template uint8_t* message_impl<Nodes>::encode<big>(const Nodes& x, uint8_t* pos);

    template <>
    template <endianness E>
    bool message_impl<Nodes>::decode(Nodes& x, const uint8_t*& pos, const uint8_t* end)
    {
        return (
            do_decode_resize<E, uint32_t>(x.nodes, pos, end, 3) &&
            do_decode_in_place<E>(x.nodes.data(), x.nodes.size(), pos, end) &&
            do_decode_advance(12, pos, end)
        );
    }
    template bool message_impl<Nodes>::decode<native>(Nodes& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Nodes>::decode<little>(Nodes& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Nodes>::decode<big>(Nodes& x, const uint8_t*& pos, const uint8_t* end);

    template <>
    void message_impl<Nodes>::print(const Nodes& x, std::ostream& out, size_t indent)
    {
        do_print(out, indent, "nodes", x.nodes.data(), std::min(x.nodes.size(), size_t(3)));
    }
    template void message_impl<Nodes>::print(const Nodes& x, std::ostream& out, size_t indent);

    template <>
    template <endianness E>
    uint8_t* message_impl<Token>::encode(const Token& x, uint8_t* pos)
    {
        pos = do_encode<E>(pos, x.discriminator);
        switch (x.discriminator)
        {
            case Token::discriminator_id: do_encode<E>(pos, x.id); break;
            case Token::discriminator_keys: do_encode<E>(pos, x.keys); break;
            case Token::discriminator_nodes: do_encode<E>(pos, x.nodes); break;
        }
        pos = pos + 16;
        return pos;
    }
    template uint8_t* message_impl<Token>::encode<native>(const Token& x, uint8_t* pos);
    template uint8_t* message_impl<Token>::encode<little>(const Token& x, uint8_t* pos);
    template uint8_t* message_impl<Token>::encode<big>(const Token& x, uint8_t* pos);

    template <>
    template <endianness E>
    bool message_impl<Token>::decode(Token& x, const uint8_t*& pos, const uint8_t* end)
    {
        if (!do_decode<E>(x.discriminator, pos, end)) return false;
        switch (x.discriminator)
        {
            case Token::discriminator_id: if (!do_decode_in_place<E>(x.id, pos, end)) return false; break;
            case Token::discriminator_keys: if (!do_decode_in_place<E>(x.keys, pos, end)) return false; break;
            case Token::discriminator_nodes: if (!do_decode_in_place<E>(x.nodes, pos, end)) return false; break;
            default: return false;
        }
        return do_decode_advance(16, pos, end);
    }
    template bool message_impl<Token>::decode<native>(Token& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Token>::decode<little>(Token& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Token>::decode<big>(Token& x, const uint8_t*& pos, const uint8_t* end);

    template <>
    void message_impl<Token>::print(const Token& x, std::ostream& out, size_t indent)
    {
        switch (x.discriminator)
        {
            case Token::discriminator_id: do_print(out, indent, "id", x.id); break;
            case Token::discriminator_keys: do_print(out, indent, "keys", x.keys); break;
            case Token::discriminator_nodes: do_print(out, indent, "nodes", x.nodes); break;
        }
    }
    template void message_impl<Token>::print(const Token& x, std::ostream& out, size_t indent);

    template <>
    template <endianness E>
    uint8_t* message_impl<Object>::encode(const Object& x, uint8_t* pos)
    {
        pos = do_encode<E>(pos, x.token);
        pos = do_encode<E>(pos, uint32_t(x.values.size()));
        pos = do_encode<E>(pos, x.values.data(), uint32_t(x.values.size()));
        pos = do_encode<E>(pos, uint32_t(x.updated_values.size()));
        pos = do_encode<E>(pos, x.updated_values.data(), uint32_t(x.updated_values.size()));
        pos = align<8>(pos);
        return pos;
    }
    template uint8_t* message_impl<Object>::encode<native>(const Object& x, uint8_t* pos);
    template uint8_t* message_impl<Object>::encode<little>(const Object& x, uint8_t* pos);
    template uint8_t* message_impl<Object>::encode<big>(const Object& x, uint8_t* pos);

    template <>
    template <endianness E>
    bool message_impl<Object>::decode(Object& x, const uint8_t*& pos, const uint8_t* end)
    {
        return (
            do_decode<E>(x.token, pos, end) &&
            do_decode_resize<E, uint32_t>(x.values, pos, end) &&
            do_decode<E>(x.values.data(), x.values.size(), pos, end) &&
            do_decode_resize<E, uint32_t>(x.updated_values, pos, end) &&
            do_decode<E>(x.updated_values.data(), x.updated_values.size(), pos, end) &&
            do_decode_align<8>(pos, end)
        );
    }
    template bool message_impl<Object>::decode<native>(Object& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Object>::decode<little>(Object& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Object>::decode<big>(Object& x, const uint8_t*& pos, const uint8_t* end);

    template <>
    void message_impl<Object>::print(const Object& x, std::ostream& out, size_t indent)
    {
        do_print(out, indent, "token", x.token);
        do_print(out, indent, "values", x.values.data(), x.values.size());
        do_print(out, indent, "updated_values", std::make_pair(x.updated_values.data(), x.updated_values.size()));
    }
    template void message_impl<Object>::print(const Object& x, std::ostream& out, size_t indent);

    template <>
    template <endianness E>
    uint8_t* message_impl<Values>::encode(const Values& x, uint8_t* pos)
    {
        pos = do_encode<E>(pos, x.transaction_id);
        pos = do_encode<E>(pos, uint32_t(x.objects.size()));
        pos = do_encode<E>(pos, x.objects.data(), uint32_t(x.objects.size()));
        return pos;
    }
    template uint8_t* message_impl<Values>::encode<native>(const Values& x, uint8_t* pos);
    template uint8_t* message_impl<Values>::encode<little>(const Values& x, uint8_t* pos);
    template uint8_t* message_impl<Values>::encode<big>(const Values& x, uint8_t* pos);

    template <>
    template <endianness E>
    bool message_impl<Values>::decode(Values& x, const uint8_t*& pos, const uint8_t* end)
    {
        return (
            do_decode<E>(x.transaction_id, pos, end) &&
            do_decode_resize<E, uint32_t>(x.objects, pos, end) &&
            do_decode<E>(x.objects.data(), x.objects.size(), pos, end)
        );
    }
    template bool message_impl<Values>::decode<native>(Values& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Values>::decode<little>(Values& x, const uint8_t*& pos, const uint8_t* end);
    template bool message_impl<Values>::decode<big>(Values& x, const uint8_t*& pos, const uint8_t* end);

    template <>
    void message_impl<Values>::print(const Values& x, std::ostream& out, size_t indent)
    {
        do_print(out, indent, "transaction_id", x.transaction_id);
        do_print(out, indent, "objects", x.objects.data(), x.objects.size());
    }
    template void message_impl<Values>::print(const Values& x, std::ostream& out, size_t indent);

    } // namespace detail
    } // namespace prophy

Write and read
------------------

We can create a program which fills message with data, encodes it,
then decodes buffer to another instance of message and prints it::

    #include <stdio.h>
    #include <iostream>
    #include "values.ppf.hpp"

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

    using namespace prophy::generated;

    int main()
    {
        Values msg;
        msg.transaction_id = 1234;
        msg.objects.emplace_back();
        msg.objects.emplace_back(Object{{Token::discriminator_keys_t, {1, 2, 3}}, {1, 2, 3, 4, 5}, {'\x0e'}});

        std::vector<uint8_t> data = msg.encode();
        print_bytes(data.data(), data.size());

        Values msg2;
        msg2.decode(data);
        std::cout << msg2.print();
        return 0;
    }

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
