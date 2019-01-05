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


LOREM_W_BREAKS = "\n".join([
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt "
    "ut labore et dolore magna aliqua. Libero nunc consequat interdum varius sit. Maecenas accumsan "
    "lacus vel facilisis:",
    "  - Dui ut ornare,",
    "  - Lectus,",
    "  - Malesuada pellentesque,",
    "",
    "",
    "Elit eget gravida cum sociis natoque penatibus et. Netus et malesuada fames ac turpis egestas sed.",
    "Egestas integer eget aliquet.",
])

FOO_GEN_TEST = [
    ("", 0, ""),
    ("At duis convallis eget gravida cum sociis.", 0,
     """\
.... Foo writes: .......................
l0x00: At duis convallis eget gravida
       cum sociis.
"""),
    ("At duis convallis eget gravida cum sociis.", 1,
     """\
    .... Foo writes: ...................
    l0x00: At duis convallis eget
           gravida cum sociis.
"""),
    ("At duis convallis eget gravida cum sociis.", 4,
     """\
                .... Foo writes: .......
                l0x00: At duis convallis
                       eget gravida cum
                       sociis.
"""),

    (LOREM_W_BREAKS, 0,
     """\
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
"""
     ),
    (LOREM_W_BREAKS, 2,
     """\
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
     ),
]


@pytest.mark.parametrize("input_str, level, reference_str", FOO_GEN_TEST)
def test_foo_generator(foo_generator, input_str, level, reference_str):
    assert render_str(foo_generator, input_str, level) == reference_str


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


def test_c_generator_0(c_alike_generator):
    input_str = LOREM_W_BREAKS
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
    assert render_str(c_alike_generator, input_str, 0) == reference_str


def test_c_generator_2(c_alike_generator):
    input_str = LOREM_W_BREAKS
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
    assert render_str(c_alike_generator, input_str, 2) == reference_str


def render_str(gen_, input_str, indent_level):
    return "".join(gen_(input_str, indent_level=indent_level))


@pytest.fixture
def kak_block_generator():
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


def test_empty_text_word_wrap(kak_block_generator):
    assert "".join(kak_block_generator("", indent_level=0)) == """\
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


def test_single_line_slpit_0(kak_block_generator):
    assert "".join(kak_block_generator(LOREM_SINGLE_LINE, indent_level=0)) == """\
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
"""


def test_single_line_slpit_1(kak_block_generator):
    assert "".join(kak_block_generator(LOREM_SINGLE_LINE, indent_level=1)) == """\
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
"""


def test_single_line_slpit_2(kak_block_generator):
    assert "".join(kak_block_generator(LOREM_SINGLE_LINE, indent_level=2)) == """\
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
"""


def test_multi_line_slpit_long(kak_block_generator):
    assert "".join(kak_block_generator(LOREM_W_BREAKS, indent_level=3)) == """\
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
             | lacus vel facilisis:
             %    - Dui ut ornare,
             %    - Lectus,
             %    - Malesuada
             | pellentesque,
             % Elit eget gravida cum
             | sociis natoque penatibus
             | et. Netus et malesuada
             | fames ac turpis egestas
             | sed.
             % Egestas integer eget
             | aliquet.
             % :fooing end<
             % ^^^^^^^^^^^^^^^^^^^^^^^^^
"""
