import pytest

from prophyc.generators import word_wrap


# flake8: noqa W291


@pytest.fixture
def foo_generator():
    foo_breaker = word_wrap.BreakLinesByWidth(
        max_line_width=40,
        soft_indent_tail=" " * 7,
    )

    @foo_breaker
    def foo_writer(raw_paragraphs):
        if raw_paragraphs:
            foo_breaker.make_a_bar(".", "Foo writes:")
            for line_index, line in enumerate(raw_paragraphs.split("\n")):
                yield "l0x{:02X}: {}".format(line_index, line)

    return foo_writer


FOO_GEN_TEST = ["""\
.... Foo writes: .......................
l0x00: Lorem ipsum dolor sit amet,
       consectetur adipiscing elit, sed
       do eiusmod tempor incididunt ut
       labore et dolore magna aliqua.
       Libero nunc consequat interdum
       varius sit. Maecenas accumsan
       lacus vel facilisis:
l0x01:   - Dui ut ornare,
l0x02:   - Lectus,
l0x03:   - Malesuada pellentesque,
l0x04: 
l0x05: 
l0x06: Elit eget gravida cum sociis
       natoque penatibus et. Netus et
       malesuada fames ac turpis egestas
       sed.
l0x07: Egestas integer eget aliquet.
""", """\
    .... Foo writes: ...................
    l0x00: Lorem ipsum dolor sit amet,
           consectetur adipiscing elit,
           sed do eiusmod tempor
           incididunt ut labore et
           dolore magna aliqua. Libero
           nunc consequat interdum
           varius sit. Maecenas accumsan
           lacus vel facilisis:
    l0x01:   - Dui ut ornare,
    l0x02:   - Lectus,
    l0x03:   - Malesuada pellentesque,
    l0x04: 
    l0x05: 
    l0x06: Elit eget gravida cum sociis
           natoque penatibus et. Netus
           et malesuada fames ac turpis
           egestas sed.
    l0x07: Egestas integer eget aliquet.
""", """\
        .... Foo writes: ...............
        l0x00: Lorem ipsum dolor sit
               amet, consectetur
               adipiscing elit, sed do
               eiusmod tempor incididunt
               ut labore et dolore magna
               aliqua. Libero nunc
               consequat interdum varius
               sit. Maecenas accumsan
               lacus vel facilisis:
        l0x01:   - Dui ut ornare,
        l0x02:   - Lectus,
        l0x03:   - Malesuada
               pellentesque,
        l0x04: 
        l0x05: 
        l0x06: Elit eget gravida cum
               sociis natoque penatibus
               et. Netus et malesuada
               fames ac turpis egestas
               sed.
        l0x07: Egestas integer eget
               aliquet.
"""

                ]


@pytest.mark.parametrize("level, reference_str", enumerate(FOO_GEN_TEST),
                         ids=[str(i) for i in range(len(FOO_GEN_TEST))])
def test_foo_generator(foo_generator, lorem_with_breaks, level, reference_str):
    assert render_str(foo_generator, lorem_with_breaks, level) == reference_str


@pytest.fixture
def c_breaker():
    c_breaker = word_wrap.BreakLinesByWidth(
        40, "    ", "/* ", " * ", "   ", " */"
    )
    return c_breaker


def test_c_breaker1(c_breaker):
    @c_breaker
    def my_gen():
        c_breaker.make_a_bar(title="that bar")
        yield "thing"
        c_breaker.make_a_bar(".", title="sub bar 1")
        c_breaker.make_a_bar(".", title="sub bar 2")
        yield "multi\nline\nparagraph"

    assert "".join(my_gen(indent_level=2)) == """\
        /* ==== that bar ===============
         * thing
         * .... sub bar 1 ..............
         * .... sub bar 2 ..............
         * multi
           line
           paragraph
         */"""


def test_c_breaker2(c_breaker):
    @c_breaker
    def my_gen():
        c_breaker.make_a_bar(title="that bar")
        return iter(())

    assert "".join(my_gen(indent_level=2)) == """\
        /* ==== that bar ===============
         */"""


def test_c_breaker3(c_breaker):
    @c_breaker
    def my_gen():
        return iter(())

    assert "".join(my_gen(indent_level=2)) == """\
        /*  */"""


@pytest.fixture
def c_alike_generator(c_breaker):
    @c_breaker
    def c_writer(raw_paragraphs):
        for line in raw_paragraphs.split("\n"):
            yield line

    return c_writer


@pytest.mark.parametrize("indent, expected_result", enumerate([
    "/*  */",
    "    /*  */",
    "        /*  */",
    "            /*  */",
]))
def test_c_generator_empty(c_alike_generator, indent, expected_result):
    assert render_str(c_alike_generator, "", indent) == expected_result


def test_wraps_with_overflow(c_alike_generator):
    input_str = (
        "Lorem ipsum dolor sit amet, consecteturadipiscingelitseddoeiusmodtempor ut "
        "labore et dolore magna aliqua. Liberonuncconsequatinterdumvariussit. Maecenas accumsan lacus")

    assert render_str(c_alike_generator, input_str, 3) == """\
            /* Lorem ipsum dolor sit
               amet,
               consecteturadipiscingelitseddoeiusmodtempor
               ut labore et dolore magna
               aliqua.
               Liberonuncconsequatinterdumvariussit.
               Maecenas accumsan lacus
             */"""


def test_c_generator_0(c_alike_generator, lorem_with_breaks):
    reference_str = """\
/* Lorem ipsum dolor sit amet,
   consectetur adipiscing elit, sed do
   eiusmod tempor incididunt ut labore
   et dolore magna aliqua. Libero nunc
   consequat interdum varius sit.
   Maecenas accumsan lacus vel
   facilisis:
 *    - Dui ut ornare,
 *    - Lectus,
 *    - Malesuada pellentesque,
 * Elit eget gravida cum sociis natoque
   penatibus et. Netus et malesuada
   fames ac turpis egestas sed.
 * Egestas integer eget aliquet.
 */"""
    assert render_str(c_alike_generator, lorem_with_breaks, 0) == reference_str


def test_c_generator_2(c_alike_generator, lorem_with_breaks):
    reference_str = """\
        /* Lorem ipsum dolor sit amet,
           consectetur adipiscing elit,
           sed do eiusmod tempor
           incididunt ut labore et
           dolore magna aliqua. Libero
           nunc consequat interdum
           varius sit. Maecenas accumsan
           lacus vel facilisis:
         *    - Dui ut ornare,
         *    - Lectus,
         *    - Malesuada pellentesque,
         * Elit eget gravida cum sociis
           natoque penatibus et. Netus
           et malesuada fames ac turpis
           egestas sed.
         * Egestas integer eget aliquet.
         */"""
    assert render_str(c_alike_generator, lorem_with_breaks, 2) == reference_str


def render_str(gen_, input_str, indent_level):
    return "".join(gen_(input_str, indent_level=indent_level))


@pytest.fixture
def fooing_gen():
    breaker = word_wrap.BreakLinesByWidth(
        max_line_width=40,
        hard_indent_tail=" % ",
        soft_indent_tail=" | ",
    )

    @breaker
    def fooing(raw_paragraphs):
        breaker.make_a_bar("=", "that things")
        yield ">fooing start:"
        for line in raw_paragraphs.split("\n"):
            yield line

        yield ":fooing end<"
        breaker.make_a_bar("^")

    return fooing


def test_empty_text_word_wrap(fooing_gen):
    assert "".join(fooing_gen("", indent_level=0)) == """\
 % ==== that things ====================
 % >fooing start:
 % :fooing end<
 % ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
"""


LOREM_SINGLE_LINE = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
    "ut labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan "
    "lacus vel facilisis.\n"
)

FOOING_TEST = [
    """\
 % ==== that things ====================
 % >fooing start:
 % Lorem ipsum dolor sit amet,
 | consectetur adipiscing elit, sed do
 | eiusmod tempor incididunt ut labore
 | et dolore magna aliqua. Libero nunc
 | consequat interdum varius sit.
 | Maecenas accumsan lacus vel
 | facilisis.
 % :fooing end<
 % ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""", """\
     % ==== that things ================
     % >fooing start:
     % Lorem ipsum dolor sit amet,
     | consectetur adipiscing elit, sed
     | do eiusmod tempor incididunt ut
     | labore et dolore magna aliqua.
     | Libero nunc consequat interdum
     | varius sit. Maecenas accumsan
     | lacus vel facilisis.
     % :fooing end<
     % ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""", """\
         % ==== that things ============
         % >fooing start:
         % Lorem ipsum dolor sit amet,
         | consectetur adipiscing elit,
         | sed do eiusmod tempor
         | incididunt ut labore et
         | dolore magna aliqua. Libero
         | nunc consequat interdum
         | varius sit. Maecenas accumsan
         | lacus vel facilisis.
         % :fooing end<
         % ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
""", """\
             % ==== that things ========
             % >fooing start:
             % Lorem ipsum dolor sit
             | amet, consectetur
             | adipiscing elit, sed do
             | eiusmod tempor incididunt
             | ut labore et dolore magna
             | aliqua. Libero nunc
             | consequat interdum varius
             | sit. Maecenas accumsan
             | lacus vel facilisis.
             % :fooing end<
             % ^^^^^^^^^^^^^^^^^^^^^^^^^
"""
]


@pytest.mark.parametrize("indent, reference_str", enumerate(FOOING_TEST), ids=[str(i) for i in range(len(FOOING_TEST))])
def test_single_line_slpit_0(fooing_gen, indent, reference_str):
    assert "".join(fooing_gen(LOREM_SINGLE_LINE, indent_level=indent)) == reference_str


@pytest.mark.parametrize("string", [
    "", " ", "\n", "abcd", "abcd efgh", "abcd\nefgh", "\nabcd\nefgh\n", "\n \t \n"
])
def test_split_short_string_not_modified(string):
    assert "".join(word_wrap.split_long_string(string)) == string


def test_split_string_with_short_lines():
    INPUT = """\
 | Lorem ipsum dolor sit
 | amet, consectetur
 | adipiscing elit, sed do
 | eiusmod tempor incididunt
 | ut labore et dolore magna
 | aliqua.
"""
    assert list(word_wrap.split_long_string(INPUT)) == [
        ' | Lorem ipsum dolor sit\n',
        ' | amet, consectetur\n',
        ' | adipiscing elit, sed do\n',
        ' | eiusmod tempor incididunt\n',
        ' | ut labore et dolore magna\n',
        ' | aliqua.\n',
        ''
    ]


def test_breaking_long_string_no_breaks():
    parts = list(word_wrap.split_long_string(LOREM_SINGLE_LINE))
    assert "".join(parts) == LOREM_SINGLE_LINE
    assert parts == [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ',
        'ut labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas ',
        'accumsan lacus vel facilisis.\n'
    ]


def test_breaking_long_string(lorem_with_breaks):
    parts = list(word_wrap.split_long_string(lorem_with_breaks))
    assert "".join(parts) == lorem_with_breaks
    assert parts == [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ',
        'ut labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas ',
        'accumsan lacus vel facilisis:\n  - Dui ut ornare,\n  - Lectus,\n  - Malesuada pellentesque,\n\n\nElit ',
        'eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis ',
        'egestas sed.\nEgestas integer eget aliquet.'
    ]


def test_hard_breaking_string():
    text = "".join(chr(c) for s, e in ('AZ', '09', 'az') * 4 for c in range(ord(s), ord(e)))
    parts = list(word_wrap.split_long_string(text))
    assert "".join(parts) == text
    assert parts == [
        'ABCDEFGHIJKLMNOPQRSTUVWXY012345678abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTU',
        'VWXY012345678abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY012345678abcdefgh',
        'ijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY012345678abcdefghijklmnopqrstuvwxy'
    ]
