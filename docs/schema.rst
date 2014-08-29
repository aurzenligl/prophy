Schema language
-----------------

Prophy schema features following built-in types:

- ``i8``, signed 1-byte integer,
- ``i16``, signed 2-byte integer,
- ``i32``, signed 4-byte integer,
- ``i64``, signed 8-byte integer,
- ``u8``, unsigned 1-byte integer,
- ``u16``, unsigned 2-byte integer,
- ``u32``, unsigned 4-byte integer,
- ``u64``, unsigned 8-byte integer,
- ``float``, 32-bit floating number,
- ``double``, 64-bit floating double-precision number,

Prophy allows to define constants::

    const MY_MIN = -1
    const MY_MAX = 0xFFF

typedefs::

    typedef u32 my_new_int;

enums::

    enum MyEnum
    {
        MyEnum_1 = 1,
        MyEnum_2 = 2,
        MyEnum_3 = 3
    }

structs::

    struct MyStruct
    {
        u32 x;
    };

Structs may contain arrays, which can be:

- fixed: fixed-length::

    struct MyStruct
    {
        u32 x[10];
    };

- dynamic: variable-length::

    struct MyStruct
    {
        u32 x<>;
    };

- limited: variable-length with maximum number of elements and fixed-length on wire::

    struct MyStruct
    {
        u32 x<10>;
    };

- greedy: encoded to wire without delimiter indicating length,
  any struct could contain only one such array as the last field::

    struct MyStruct
    {
        u32 x<...>;
    };

Struct can contain bytes fields, which are byte arrays coming in the same 4 flavors::

    struct MyStruct
    {
        bytes a[10];
        bytes b<>;
        bytes c<10>;
        bytes d<...>;
    };

Struct field can be optional::

    struct MyStruct
    {
        u32* x;
    };

Discriminated unions, which may have hardcoded numbers, constants or enumerators as discriminators::

    union MyUnion
    {
        1: i8 a;
        2: u64 b;
        3: SomeType c;
    };

Currently there are no includes or namespaces in the language.
