from prophyc.generators import word_wrap
from prophyc.generators.base import GeneratorBase, TranslatorBase

libname = u"prophy"
primitive_types = {x + y: u"%s.%s" % (libname, x + y) for x in u"uir" for y in ["8", "16", "32", "64"]}
primitive_types['byte'] = u'%s.u8' % libname


def _make_list(repr_function, members):
    if not members:
        return u"[]"
    return u"[%s\n    ]" % "".join(u"\n        %s," % repr_function(e) for e in members)


def _form_enum_member(member):
    return u"('%s', %s)" % (member.name, member.value)


def _generate_enum_constants(members):
    return u"\n".join((u"%s = %s" % (member.name, member.value) for member in members))


def _form_struct_member(member):
    prefixed_type = primitive_types.get(member.type_name, member.type_name)
    if member.optional:
        prefixed_type = u"%s.optional(%s)" % (libname, prefixed_type)
    if member.is_array:
        elem_strs = []
        if member.bound:
            elem_strs.append(u"bound='%s'" % member.bound)
        if member.size:
            elem_strs.append(u"size=%s" % member.size)
        if member.type_name == 'byte':
            prefixed_type = u'%s.bytes(%s)' % (libname, ', '.join(elem_strs))
        else:
            prefixed_type = u'%s.array(%s)' % (libname, ', '.join([prefixed_type] + elem_strs))
    return u"('%s', %s)" % (member.name, prefixed_type)


def _form_union_member(member):
    prefixed_type = u"%s.%s" % (libname, member.type_name) if member.type_name in primitive_types else member.type_name
    return u"('%s', %s, %s)" % (member.name, prefixed_type, member.discriminator)


def _indent(text, prefix):
    return ''.join(prefix + line for line in text.splitlines(True))


import_breaker = word_wrap.BreakLinesByWidth(80, "    ", "", "    ", "    ")


class _PythonTranslator(TranslatorBase):
    block_template = u"""\
# -*- encoding: utf-8 -*-
# This file has been generated by prophyc.

import sys

import {0}

{{content}}""".format(libname)

    def __init__(self):
        self.included_symbols = set()

    def __call__(self, nodes, base_name):
        self.included_symbols = set()
        return super(_PythonTranslator, self).__call__(nodes, base_name)

    def translate_include(self, include):
        included = list(sorted(n.name for n in include.defined_symbols() if n.name not in self.included_symbols))
        self.included_symbols.update(included)
        if not included:
            return u""

        def translate(relative_import_indicator):
            statement_begin = u"from %s%s import " % (relative_import_indicator, include.name.split("/")[-1])
            symbols = u", ".join(included)
            if len(statement_begin) + len(symbols) <= 80:
                return statement_begin + symbols

            @import_breaker
            def importer():
                yield symbols

            return u"%s(\n%s)" % (statement_begin, "".join(importer()))

        return """\
if sys.version_info < (3,):
%s
else:
%s""" % (_indent(translate(''), '    '), _indent(translate('.'), '    '))

    @staticmethod
    def translate_constant(constant):
        content = u"%s = %s" % (constant.name, constant.value)
        doc = constant.docstring
        if doc:
            content = u"\'\'\'{}\'\'\'\n{}".format(doc, content)
        return content

    @staticmethod
    def translate_typedef(typedef):
        if typedef.type_name in primitive_types:
            value = u"{0}.{1}".format(libname, typedef.type_name)
        else:
            value = typedef.type_name

        return u"%s = %s" % (typedef.name, value)

    @staticmethod
    def translate_enum(enum):
        members_list = _make_list(_form_enum_member, enum.members)
        constants_list = _generate_enum_constants(enum.members)
        template = u"""\
class {enum_name}({libname}.with_metaclass({libname}.enum_generator, {libname}.enum)):
    _enumerators = {members_list}


{constants}"""
        return template.format(libname=libname, enum_name=enum.name, members_list=members_list,
                               constants=constants_list)

    @staticmethod
    def translate_struct(struct):
        members_list = _make_list(_form_struct_member, struct.members)
        template = u"""\
class {struct_name}({libname}.with_metaclass({libname}.struct_generator, {libname}.struct)):
    _descriptor = {members_list}"""
        return template.format(libname=libname, struct_name=struct.name, members_list=members_list)

    @staticmethod
    def translate_union(union):
        members_list = _make_list(_form_union_member, union.members)
        union_template = u"""\
class {union_name}({libname}.with_metaclass({libname}.union_generator, {libname}.union)):
    _descriptor = {members_list}"""
        return union_template.format(libname=libname, union_name=union.name, members_list=members_list)

    @classmethod
    def _make_lines_splitter(cls, previous_node_type, current_node_type):
        if not previous_node_type:
            return u""

        if previous_node_type == "Include" and current_node_type != "Include":
            return u"\n\n"

        if previous_node_type in ("Struct", "Union") or current_node_type in ("Enum", "Struct", "Union"):
            return u"\n\n\n"

        if previous_node_type == "Enum" and current_node_type == "Constant":
            # Enum ends with several constants, so they join as the same type
            return u"\n"

        if previous_node_type != current_node_type:
            return u"\n\n"

        return u"\n"


class PythonGenerator(GeneratorBase):
    top_level_translators = {
        ".py": _PythonTranslator
    }
