import os

class PythonSerializer(object):

    libname = "prophy"
    primitive_types = {"u8", "u16", "u32", "u64",
                       "i8", "i16", "i32", "i64",
                       "r32", "r64"}

    def __init__(self, output_dir = "."):
        self.output_dir = output_dir

    def serialize_string(self, dataHolder, no_prolog = False):
        return os.linesep.join(filter(None, (None if no_prolog else self.__render_prolog(),
                                             self.__render_includes(dataHolder.includes),
                                             self.__render_constants(dataHolder.constants),
                                             self.__render_typedefs(dataHolder.typedefs, dataHolder.structs, dataHolder.enums),
                                             self.__render_enums(dataHolder.enums),
                                             self.__render_structs(dataHolder.structs))))

    def serialize(self, dataHolder, basename):
        path = os.path.join(self.output_dir, basename + ".py")
        out = self.serialize_string(dataHolder)
        open(path, "w").write(out)

    def __render_prolog(self):
        return """\
import %s

def bitMaskOr(x, y):
    return x | y

def shiftLeft(x, y):
    return x << y
""" % self.libname

    def __render_enum_members(self, members):
        return (",\n" + " " * 21).join(("('%s', %s)" % (name, value) for name, value in members))

    def __render_enum_constants(self, members):
        return "\n".join(("%s = %s" % (name, value) for name, value in members))

    def __render_enums(self, enums):
        return "\n".join((("class {1}({0}.enum):\n"
                           "    __metaclass__ = {0}.enum_generator\n"
                           "    _enumerators  = [{2}]\n"
                           "\n"
                           "{3}\n").format(self.libname, name, self.__render_enum_members(members), self.__render_enum_constants(members))
                           for name, members in enums))

    def __render_typedef(self, typedef, structs, enums, used_structs, used_enums):
        prefix = ""
        key, val = typedef
        if val.startswith('u') or val.startswith('i') or val.startswith('r'):
            val = self.libname + "." + val
        elif val.startswith('S'):
            if val not in used_structs:
                prefix = self._get_struct_for_typedef(val, structs) + '\n'
            used_structs.append(val)
        elif val.startswith('E'):
            if val not in used_enums:
                prefix = self._get_enum_for_typedef(val, enums) + '\n'
            used_enums.append(val)
        return "%s%s = %s" % (prefix, key, val)

    def __render_typedefs(self, typedefs, structs, enums):
        used_structs = []
        used_enums = []
        return "".join((self.__render_typedef(typedef, structs, enums, used_structs, used_enums) + "\n" for typedef in typedefs))

    def _get_struct_for_typedef(self, val, struct_list):
        out = ""
        for i in xrange(len(struct_list)):
            if struct_list[i].name == val:
                x = struct_list.pop(i)
                return self.__render_structs([x])
        return ""

    def _get_enum_for_typedef(self, val2, enums):
        out = ""
        for key, val in enums:
            if key == val2:
                enums.remove((key, val))
                return self.__render_enums([(key, val)])
        return ""

    def __render_includes(self, includes):
        return "".join(("from %s import *\n" % include for include in includes))

    def __render_constants(self, constants):
        return "".join(("%s = %s\n" % constant for constant in constants))

    def _serialize_union(self, union_dict):
        def serialize_union_members(list):
            desc = []
            for member in list:
                    k, v = member
                    desc.append("('{0}',{1})" .format(v, k))
            return ", ".join(desc)
        out = ""

        for key, val in union_dict.iteritems():
            out += "class {0}({1}.union):" .format(key, self.libname) + "\n"
            out += "    __metaclass__ = {0}.union_generator" .format(self.libname) + "\n"
            out += "    _discriminator = EDisc{0}" .format(key) + "\n"
            out += "    _descriptor  = [" + serialize_union_members(val.list) + "]\n"

        return out

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
                "    _descriptor = [{2}]\n").format(self.libname, struct.name, self.__render_struct_members(struct.members))

    def __render_structs(self, structs):
        return "\n".join(self.__render_struct(struct) for struct in structs)

