import os

from prophyc import model

libname = "prophy"
primitive_types = {x + y : "%s.%s" % (libname, x + y) for x in "uir" for y in ["8", "16", "32", "64"]}
primitive_types['byte'] = '%s.u8' % libname

def _generate_include(include):
    return "from %s import *\n" % include

def _generate_constant(constant):
    return "%s = %s\n" % constant

def _generate_typedef(typedef):
    return "%s = %s\n" % (typedef.name, ".".join((libname, typedef.type))
                                        if typedef.type in primitive_types
                                        else typedef.type)

def _generate_enum_members(members):
    return (",\n" + " " * 21).join(("('%s', %s)" % (name, value) for name, value in members))

def _generate_enum_constants(members):
    return "\n".join(("%s = %s" % (name, value) for name, value in members))

def _generate_enum(enum):
    return ("class {1}({0}.enum):\n"
            "    __metaclass__ = {0}.enum_generator\n"
            "    _enumerators  = [{2}]\n"
            "\n"
            "{3}\n").format(libname,
                            enum.name,
                            _generate_enum_members(enum.members),
                            _generate_enum_constants(enum.members))

def _generate_struct_member(member):
    prefixed_type = primitive_types.get(member.type, member.type)
    if member.optional:
        prefixed_type = "%s.optional(%s)" % (libname, prefixed_type)
    if member.array:
        elem_strs = []
        if member.array_bound:
            elem_strs.append("bound = '%s'" % member.array_bound)
        if member.array_size:
            elem_strs.append("size = %s" % member.array_size)
        if member.type == 'byte':
            prefixed_type = '%s.bytes(%s)' % (libname, ', '.join(elem_strs))
        else:
            prefixed_type = '%s.array(%s)' % (libname, ', '.join([prefixed_type] + elem_strs))
    return "('%s', %s)" % (member.name, prefixed_type)

def _generate_struct_members(keys):
    return (",\n" + " " * 19).join((_generate_struct_member(member) for member in keys))

def _generate_struct(struct):
    return ("class {1}({0}.struct):\n"
            "    __metaclass__ = {0}.struct_generator\n"
            "    _descriptor = [{2}]\n").format(libname,
                                                struct.name,
                                                _generate_struct_members(struct.members))

def _generate_union_member(member):
    prefixed_type = ".".join((libname, member.type)) if member.type in primitive_types else member.type
    return "('%s', %s, %s)" % (member.name, prefixed_type, member.discriminator)

def _generate_union_members(members):
    return (",\n" + " "*19).join(_generate_union_member(member) for member in members)

def _generate_union(union):
    return ("class {1}({0}.union):\n"
            "    __metaclass__ = {0}.union_generator\n"
            "    _descriptor = [{2}]\n").format(libname,
                                                union.name,
                                                _generate_union_members(union.members))

generate_visitor = {
    model.Include: _generate_include,
    model.Constant: _generate_constant,
    model.Typedef: _generate_typedef,
    model.Enum: _generate_enum,
    model.Struct: _generate_struct,
    model.Union: _generate_union
}

def _generate(node):
    return generate_visitor[type(node)](node)

class PythonGenerator(object):

    def __init__(self, output_dir = "."):
        self.output_dir = output_dir

    def generate_definitions(self, nodes):
        return "\n".join(_generate(node) for node in nodes)

    def serialize_string(self, nodes):
        header = "import {}\n".format(libname)
        definitions = self.generate_definitions(nodes)
        if not definitions:
            return header
        return header + "\n" + definitions

    def serialize(self, nodes, basename):
        path = os.path.join(self.output_dir, basename + ".py")
        out = self.serialize_string(nodes)
        open(path, "w").write(out)
