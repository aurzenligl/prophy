.. _cpp_full:

C++ full codec
===============

This page describes how to manipulate prophy messages using C++ codec.
Codec uses value-semantics types with integral, ``array``,
``vector`` and ``optional`` fields to represent prophy structs and unions.
These types have means to size, encode, decode and print represented messages.

Codec is nicknamed "full" as opposed to "raw" one, which allows to
form an encoded message way faster but requires moderate amount of user code
and attention.

Compilation
----------------

Prophy Compiler can be used to generate C++ full codec source code from .prophy files.
This generated code together with C++ prophy header-only library can be used
to handle Prophy messages.

Example compiler invocation::

    prophyc --cpp_full_out . test.prophy

will result in creating ``test.ppf.hpp`` and ``test.ppf.cpp``.

Generated code
----------------

All types in generated C++ code are enclosed in ``prophy::generated`` namespace.

.. note::

    ``array`` and ``optional`` class templates shipped with C++ prophy library
    are derived from ``std`` and ``boost`` implementations,
    for the sake of making library independent of C++11 std lib or boost libraries.

Enums are represented as regular C++ enums::

    enum Test1
    {
        Test1_1 = 1,
        Test1_2 = 2,
        Test1_3 = 3
    };

.. code-block:: cpp

    enum Test1
    {
        Test1_1 = 1,
        Test1_2 = 2,
        Test1_3 = 3
    };

Structs and unions are represented as value-semantics types inheriting
self-specialized ``prophy::detail::message`` class template (CRTP),
thus fulfill the API of prophy message:

.. code-block:: cpp

    template <class T>
    struct message
    {
        template <endianness E>
        size_t encode(void* data) const;

        size_t encode(void* data) const;

        template <endianness E>
        std::vector<uint8_t> encode() const;

        std::vector<uint8_t> encode() const;

        template <endianness E>
        bool decode(const void* data, size_t size);

        bool decode(const void* data, size_t size);

        template <endianness E>
        bool decode(const std::vector<uint8_t>& data);

        bool decode(const std::vector<uint8_t>& data);

        std::string print() const;
    };

Encode and decode can be used as method templates to choose
specific ``prophy::endianness`` to process data or as regular methods,
which use ``native`` endianness (actual machine endianness):

.. code-block:: cpp

    enum endianness
    {
        native,
        little,
        big
    };

Structs are represented as C++ structs with corresponding fields::

    struct Test2
    {
        u32 a;
    };

.. code-block:: cpp

    struct Test2 : public prophy::detail::message<Test2>
    {
        enum { encoded_byte_size = 4 };

        uint32_t a;

        Test2(): a() { }
        Test2(uint32_t _1): a(_1) { }

        size_t get_byte_size() const
        {
            return 4;
        }
    };

Arrays are represented as ``array`` or ``vector``.
In case of limited arrays - exceeding limit is not
prohibited, but encoding will serialize only elements up to limit::

    struct Test8
    {
        i32 a[3];
        i32 b<>;
        i32 c<3>;
        i32 d<...>;
    };

.. code-block:: cpp

    struct Test8 : public prophy::detail::message<Test8>
    {
        enum { encoded_byte_size = -1 };

        array<int32_t, 3> a;
        std::vector<int32_t> b;
        std::vector<int32_t> c; /// limit 3
        std::vector<int32_t> d; /// greedy

        Test8(): a() { }
        Test8(const array<int32_t, 3>& _1, const std::vector<int32_t>& _2, const std::vector<int32_t>& _3, const std::vector<int32_t>& _4): a(_1), b(_2), c(_3), d(_4) { }

        size_t get_byte_size() const
        {
            return b.size() * 4 + d.size() * 4 + 32;
        }
    };

Optional fields are represented by ``optional`` template class::

    struct Test6
    {
        u32* a;
        Test2* b;
    };

.. code-block:: cpp

    struct Test6 : public prophy::detail::message<Test6>
    {
        enum { encoded_byte_size = 16 };

        optional<uint32_t> a;
        optional<Test2> b;

        Test6() { }
        Test6(const optional<uint32_t>& _1, const optional<Test2>& _2): a(_1), b(_2) { }

        size_t get_byte_size() const
        {
            return 16;
        }
    };

Union representation is similar to struct one - it
contains all arms as independent fields.
Depending on current value of discriminator, chosen
arm will be encoded or printed.
Decoding overwrites discriminator as well as decoded arm::

    union Test7
    {
        0: u32 a;
        1: Test2 b;
    };

.. code-block:: cpp

    struct Test7 : public prophy::detail::message<Test7>
    {
        enum { encoded_byte_size = 8 };

        enum _discriminator
        {
            discriminator_a = 0,
            discriminator_b = 1
        } discriminator;

        static const prophy::detail::int2type<discriminator_a> discriminator_a_t;
        static const prophy::detail::int2type<discriminator_b> discriminator_b_t;

        uint32_t a;
        Test2 b;

        Test7(): discriminator(discriminator_a), a() { }
        Test7(prophy::detail::int2type<discriminator_a>, uint32_t _1): discriminator(discriminator_a), a(_1) { }
        Test7(prophy::detail::int2type<discriminator_b>, const Test2& _1): discriminator(discriminator_b), b(_1) { }

        size_t get_byte_size() const
        {
            return 8;
        }
    };

``discriminator_<field_name>_t`` variables are meant to facilitate C++11 brace-enclosed
initialization:

.. code-block:: cpp

    Test7 x{Test7::discriminator_a_t, 42};
    Test7 y{Test7::discriminator_b_t, {13}};
