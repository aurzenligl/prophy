from collections import namedtuple

from prophyc.generators import base

INDENT_STR = "    "

DocStr = namedtuple("DocStr", "block, inline")


def _form_doc(model_node, max_inl_docstring_len, indent_level):
    block_doc, inline_doc = "", ""
    if model_node.doc_str:
        if len(model_node.doc_str) <= max_inl_docstring_len and "\n" not in model_node.doc_str:
            inline_doc = u"  // {}".format(model_node.doc_str)

        elif model_node.doc_str:
            block_doc = u"\n" + "".join(
                _gen_multi_line_doc(model_node.doc_str, indent_level, block_header=model_node.name))

    return DocStr(block_doc, inline_doc)


def _gen_multi_line_doc(block_comment_text, indent_level=0, block_header="", max_line_width=100):
    new_line = "\n" + INDENT_STR * indent_level
    total_indent_len = len(new_line) - 1 + 3

    yield new_line + "/* "
    is_long_block = len(block_comment_text) >= 250

    if block_header and is_long_block:
        bar = "-" if indent_level else "="
        block_header = "{} {} ".format(bar * 4, block_header)
        block_header += bar * (max_line_width - total_indent_len - len(block_header))
        yield block_header + new_line + " * "

    tot = total_indent_len
    for not_first, long_line in enumerate(block_comment_text.split("\n")):
        if not_first and long_line:
            yield new_line + " * "
            tot = total_indent_len

        words = long_line.split()
        for not_last, word in enumerate(words, 1 - len(words)):
            if not word:
                continue
            if tot + len(word) > max_line_width:
                yield new_line + "   "
                tot = total_indent_len

            yield word
            tot += len(word)

            if not_last:
                yield " "
                tot += 1
    if is_long_block:
        yield new_line
    yield " */"


def _columnizer(model_node, column_splitter, max_line_width=100):
    members_table = [column_splitter(m) for m in model_node.members]
    widths = [max(len(str(r)) for r in g) for g in zip(*members_table)]
    max_inline_comment_width = max_line_width - sum(widths)

    for member, columns in zip(model_node.members, members_table):
        doc = _form_doc(member, max_inline_comment_width, indent_level=1)

        if doc.block:
            yield doc.block
        yield "\n" + INDENT_STR

        for is_not_last, (cell_width, cell_str) in enumerate(zip(widths, columns), 1 - len(columns)):

            yield cell_str

            padding = " " * (max(0, cell_width - len(cell_str)))
            if is_not_last:
                yield padding
            elif doc.inline:
                yield padding + doc.inline

    if model_node.members:
        yield "\n"


def generate_schema_container(model_node, designator, column_splitter):
    if model_node.doc_str:
        yield "".join(_gen_multi_line_doc(model_node.doc_str, indent_level=0, block_header=model_node.name))

    yield "\n{} {} {{".format(designator, model_node.name)

    yield "".join(_columnizer(model_node, column_splitter, max_line_width=100))

    yield "};"


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
            value = " = {};".format(member.value)
            return member.name, value

        return u''.join(generate_schema_container(enumerator, "enum", column_selector))

    @staticmethod
    def translate_struct(struct):
        def column_selector(member):
            type_ = member.value
            if member.optional:
                type_ += "*"

            if member.fixed:
                name = '{m.name}[{m.size}];'
            elif member.limited:
                name = '{m.name}<{m.size}>({m.bound});'
            elif member.dynamic:
                name = '{m.name}<@{m.bound}>;'
            elif member.greedy:
                name = '{m.name}<...>;'
            else:
                name = '{m.name};'

            return type_, " ", name.format(m=member)

        return ''.join(generate_schema_container(struct, "struct", column_selector))

    @staticmethod
    def translate_union(union):
        def column_selector(member):
            discriminator = "{}: ".format(member.discriminator)
            field_type = member.value
            field_name = " {};".format(member.name)
            return discriminator, field_type, field_name

        return ''.join(generate_schema_container(union, "union", column_selector))


class SchemaGenerator(base.GeneratorBase):
    top_level_translators = {
        '.prophy': SchemaTranslator,
    }
