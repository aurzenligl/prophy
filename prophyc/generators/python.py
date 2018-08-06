
from prophyc.generators.base import GeneratorBase, TranslatorBase


libname = "prophy"
primitive_types = {x + y: "%s.%s" % (libname, x + y) for x in "uir" for y in ["8", "16", "32", "64"]}
primitive_types['byte'] = '%s.u8' % libname


def _make_list(repr_function, members):
    if not members:
        return "[]"

    single_indent = " " * 4
    member_indent = 2 * single_indent

    def make_lines():
        for e in members:
            yield "\n%s%s" % (member_indent, repr_function(e))

    return "[%s\n%s]" % (",".join(make_lines()), single_indent)


def _form_enum_member(member):
    return "('%s', %s)" % (member.name, member.value)


def _generate_enum_constants(members):
    return "\n".join(("%s = %s" % (member.name, member.value) for member in members))


def _form_struct_member(member):
    prefixed_type = primitive_types.get(member.type_, member.type_)
    if member.optional:
        prefixed_type = "%s.optional(%s)" % (libname, prefixed_type)
    if member.array:
        elem_strs = []
        if member.bound:
            elem_strs.append("bound = '%s'" % member.bound)
        if member.size:
            elem_strs.append("size = %s" % member.size)
        if member.type_ == 'byte':
            prefixed_type = '%s.bytes(%s)' % (libname, ', '.join(elem_strs))
        else:
            prefixed_type = '%s.array(%s)' % (libname, ', '.join([prefixed_type] + elem_strs))
    return "('%s', %s)" % (member.name, prefixed_type)


def _form_union_member(member):
    prefixed_type = "%s.%s" % (libname, member.type_) if member.type_ in primitive_types else member.type_
    return "('%s', %s, %s)" % (member.name, prefixed_type, member.discriminator)


ENUM_TEMPLATE = """\
class {enum_name}({libname}.with_metaclass({libname}.enum_generator, {libname}.enum)):
    _enumerators = {members_list}

{constants}"""

STRUCT_TEMPLATE = """\
class {struct_name}({libname}.with_metaclass({libname}.struct_generator, {libname}.struct)):
    _descriptor = {members_list}"""

UNION_TEMPLATE = """\
class {union_name}({libname}.with_metaclass({libname}.union_generator, {libname}.union)):
    _descriptor = {members_list}"""

PYTHON_FILE_TEMPLATE = """\
import {0}

{{content}}""".format(libname)


class _PythonTranslator(TranslatorBase):
    block_template = PYTHON_FILE_TEMPLATE

    def translate_include(self, include):
        return "from %s import *" % include.name.split("/")[-1]

    def translate_constant(self, constant):
        return "%s = %s" % constant

    def translate_typedef(self, typedef):
        if typedef.type_ in primitive_types:
            value = "{0}.{1}".format(libname, typedef.type_)
        else:
            value = typedef.type_

        return "%s = %s" % (typedef.name, value)

    def translate_enum(self, enum):
        members_list = _make_list(_form_enum_member, enum.members)
        constants_list = _generate_enum_constants(enum.members)
        return ENUM_TEMPLATE.format(libname=libname, enum_name=enum.name, members_list=members_list,
                                    constants=constants_list)

    def translate_struct(self, struct):
        members_list = _make_list(_form_struct_member, struct.members)
        return STRUCT_TEMPLATE.format(libname=libname, struct_name=struct.name, members_list=members_list)

    def translate_union(self, union):
        members_list = _make_list(_form_union_member, union.members)
        return UNION_TEMPLATE.format(libname=libname, union_name=union.name, members_list=members_list)


class PythonGenerator(GeneratorBase):
    top_level_translators = {
        ".py": _PythonTranslator
    }
