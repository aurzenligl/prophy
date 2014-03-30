import os
import model

class PythonSerializer(object):

    libname = "prophy"
    primitive_types = set(x + y for x in "uir" for y in ["8", "16", "32", "64"])

    def __init__(self, output_dir = "."):
        self.output_dir = output_dir

    def serialize_string(self, dataHolder, no_prolog = False):
        return os.linesep.join(filter(None, (None if no_prolog else self.__render_prolog(),
                                             self.__render_nodes(dataHolder.nodes))))

    def serialize(self, dataHolder, basename):
        path = os.path.join(self.output_dir, basename + ".py")
        out = self.serialize_string(dataHolder)
        open(path, "w").write(out)

    def __render_include(self, include):
        return "from %s import *\n" % include

    def __render_constant(self, constant):
        return "%s = %s\n" % constant

    def __render_typedef(self, typedef):
        key, val = typedef
        if val in self.primitive_types:
            val = self.libname + "." + val
        return "%s = %s\n" % (key, val)

    def __render_enum_members(self, members):
        return (",\n" + " " * 21).join(("('%s', %s)" % (name, value) for name, value in members))

    def __render_enum_constants(self, members):
        return "\n".join(("%s = %s" % (name, value) for name, value in members))

    def __render_enum(self, enum):
        return ("class {1}({0}.enum):\n"
                "    __metaclass__ = {0}.enum_generator\n"
                "    _enumerators  = [{2}]\n"
                "\n"
                "{3}\n").format(self.libname,
                                enum.name,
                                self.__render_enum_members(enum.members),
                                self.__render_enum_constants(enum.members))

    def __render_union(self, union):
        return "%s = %s.u32\n" % (union.name, self.libname)

    def __render_struct_member(self, member):
        prefixed_type = self.libname + "." + member.type if member.type in self.primitive_types else member.type
        if member.array:
            if member.array_bound:
                return "('%s', %s.array(%s, bound = '%s'))" % (member.name, self.libname, prefixed_type, member.array_bound)
            else:
                return "('%s', %s.array(%s, size = %s))" % (member.name, self.libname, prefixed_type, member.array_size)
        else:
            return "('%s', %s)" % (member.name, prefixed_type)

    def __render_struct_members(self, keys):
        return (",\n" + " " * 19).join((self.__render_struct_member(member) for member in keys))

    def __render_struct(self, struct):
        return ("class {1}({0}.struct):\n"
                "    __metaclass__ = {0}.struct_generator\n"
                "    _descriptor = [{2}]\n").format(self.libname,
                                                    struct.name,
                                                    self.__render_struct_members(struct.members))

    render_visitor = {model.Include: __render_include,
                      model.Constant: __render_constant,
                      model.Typedef: __render_typedef,
                      model.Enum: __render_enum,
                      model.Union: __render_union,
                      model.Struct: __render_struct}

    def __render(self, node):
        return self.render_visitor[type(node)](self, node)

    def __render_nodes(self, nodes):
        return "\n".join((self.__render(node) for node in nodes))

    def __render_prolog(self):
        return """\
import %s

def bitMaskOr(x, y):
    return x | y

def shiftLeft(x, y):
    return x << y
""" % self.libname
