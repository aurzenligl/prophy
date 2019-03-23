from collections import namedtuple

from prophyc.generators import base, word_wrap

INDENT_STR = u"    "
MAX_LINE_WIDTH = 100

DocStr = namedtuple("DocStr", "block, inline")


def _form_doc(model_node, max_inl_docstring_len, indent_level):
    block_doc, inline_doc = "", ""
    if model_node.docstring:
        if len(model_node.docstring) <= max_inl_docstring_len and "\n" not in model_node.docstring:
            inline_doc = u"  // {}".format(model_node.docstring)

        elif model_node.docstring:
            block_doc = u"\n" + "".join(
                _gen_multi_line_doc(model_node.docstring, indent_level=indent_level, block_header=model_node.name))

    return DocStr(block_doc, inline_doc)


schema_line_breaker = word_wrap.BreakLinesByWidth(MAX_LINE_WIDTH, "    ", "/* ", " * ", "   ", " */")


@schema_line_breaker
def _gen_multi_line_doc(block_comment_text, indent_level=0, block_header=""):
    assert "\n" not in block_header, "Will not work with line breaks in header bar."

    if block_header:
        if len(block_comment_text) >= 250:
            schema_line_breaker.make_a_bar("-" if indent_level else "=", block_header)
        yield block_header

    for paragraph in block_comment_text.split("\n"):
        yield paragraph


def _columnizer(model_node, column_splitter, max_line_width=100):
    members_table = [column_splitter(m) for m in model_node.members]
    widths = [max(len(str(r)) for r in g) for g in zip(*members_table)]
    max_inline_comment_width = max_line_width - sum(widths)

    for member, columns in zip(model_node.members, members_table):
        doc = _form_doc(member, max_inline_comment_width, indent_level=1)

        if doc.block:
            yield doc.block
        yield u"\n" + INDENT_STR

        for is_not_last, (cell_width, cell_str) in enumerate(zip(widths, columns), 1 - len(columns)):

            yield cell_str

            padding = u" " * (max(0, cell_width - len(cell_str)))
            if is_not_last:
                yield padding
            elif doc.inline:
                yield padding + doc.inline

    if model_node.members:
        yield "\n"


def generate_schema_container(model_node, designator, column_splitter):
    if model_node.docstring:
        block_docstring = u"".join(_gen_multi_line_doc(model_node.docstring, indent_level=0,
                                                       block_header=model_node.name))
        if block_docstring:
            block_docstring += u"\n"
    else:
        block_docstring = u""
    members = u"".join(_columnizer(model_node, column_splitter, max_line_width=100))
    return u"{}{} {} {{{}}};".format(block_docstring, designator, model_node.name, members)


class SchemaTranslator(base.TranslatorBase):
    block_template = u'''{content}'''

    @staticmethod
    def translate_include(include):
        doc = _form_doc(include, 50, indent_level=0)
        return u"{d.block}#include \"{0.name}\"{d.inline}".format(include, d=doc)

    @staticmethod
    def translate_constant(constant):
        doc = _form_doc(constant, max_inl_docstring_len=50, indent_level=0)
        return u"{d.block}\n{0.name} = {0.value};{d.inline}".format(constant, d=doc)

    @staticmethod
    def translate_enum(enumerator):
        def column_selector(member):
            value = u" = {};".format(member.value)
            return member.name, value

        return generate_schema_container(enumerator, "enum", column_selector)

    @staticmethod
    def translate_struct(struct):
        def column_selector(member):
            type_ = member.value
            if member.optional:
                type_ += u"*"

            if member.is_fixed:
                name = u"{m.name}[{m.size}];"
            elif member.is_limited:
                name = u"{m.name}<{m.size}>;"
            elif member.is_dynamic:
                name = u"{m.name}<@{m.bound}>;"
            elif member.greedy:
                name = u"{m.name}<...>;"
            else:
                name = u"{m.name};"

            return type_, u" ", name.format(m=member)

        return generate_schema_container(struct, u"struct", column_selector)

    @staticmethod
    def translate_union(union):
        def column_selector(member):
            discriminator = u"{}: ".format(member.discriminator)
            field_type = member.value
            field_name = u" {};".format(member.name)
            return discriminator, field_type, field_name

        return generate_schema_container(union, u"union", column_selector)

    @classmethod
    def _make_lines_splitter(cls, previous_node_type, current_node_type):
        if not previous_node_type:
            return u""

        if previous_node_type == "Include" and current_node_type != "Include":
            return u"\n\n"

        if previous_node_type in ("Struct", "Union") or current_node_type in ("Enum", "Struct", "Union"):
            return u"\n\n\n"

        if previous_node_type != current_node_type:
            return u"\n\n"

        return u"\n"


class SchemaGenerator(base.GeneratorBase):
    top_level_translators = {
        '.prophy': SchemaTranslator,
    }
