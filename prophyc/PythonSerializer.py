import os

class PythonSerializer(object):
    def __init__(self, output_dir = "."):
        self.lib_imp = "prophy."
        self.output_dir = output_dir

    def serialize_string(self, dataHolder, no_prolog = False):
        return os.linesep.join(filter(None, (None if no_prolog else self.__render_prolog(),
                                             self.__render_includes(dataHolder.includes),
                                             self.__render_constants(dataHolder.constants),
                                             self.__render_typedefs(dataHolder.typedefs, dataHolder.struct_list, dataHolder.enums),
                                             self.__render_enums(dataHolder.enums),
                                             self._serialize_union(dataHolder.union_dict),
                                             self._serialize_msgs(dataHolder.sort_struct()),
                                             self._serialize_msgs(dataHolder.msgs_list))))

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
""" % self.lib_imp[:-1]

    def __render_enum_members(self, members):
        return (",\n" + " " * 21).join(("('%s', %s)" % (name, value) for name, value in members))

    def __render_enum_constants(self, members):
        return "\n".join(("%s = %s" % (name, value) for name, value in members))

    def __render_enums(self, enums):
        return "\n".join((("class {1}({0}enum):\n"
                           "    __metaclass__ = {0}enum_generator\n"
                           "    _enumerators  = [{2}]\n"
                           "\n"
                           "{3}\n").format(self.lib_imp, name, self.__render_enum_members(members), self.__render_enum_constants(members))
                           for name, members in enums))

    def __render_typedef(self, typedef, structs, enums, used_structs, used_enums):
        prefix = ""
        key, val = typedef
        if val.startswith('u') or val.startswith('i') or val.startswith('r'):
            val = self.lib_imp + val
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
                return self._serialize_msgs([x])
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
            out += "class {0}({1}union):" .format(key, self.lib_imp) + "\n"
            out += "    __metaclass__ = {0}union_generator" .format(self.lib_imp) + "\n"
            out += "    _discriminator = EDisc{0}" .format(key) + "\n"
            out += "    _descriptor  = [" + serialize_union_members(val.list) + "]\n"

        return out

    def _serialize_msgs(self, msgs_list):
        out = ""

        def serialize_members(keys):
            desc = []
            for member in keys:
                if member.type.startswith('u') or member.type.startswith('i') or member.type.startswith('r')  :
                    lib_imp = self.lib_imp
                else :
                    lib_imp = ""
                if len(member.list) > 0:
                    desc.append(self._serialize_msg_member(member))
                else:
                    desc.append("('{0}',{1}{2})" .format(member.name , lib_imp, member.type))
            return ", ".join(desc)
        for key in msgs_list:
            out += "class {0}({1}struct):" .format(key.name, self.lib_imp) + "\n"
            out += "    __metaclass__ = {0}struct_generator" .format(self.lib_imp) + "\n"
            out += "    _descriptor = [" + serialize_members(key.get_list()) + "]\n"
        return out

    def _serialize_msg_member(self, member):
        def format_simple_list(a, b):
            return  "('{0}',{1}), " .format(a, b)
        def format_array(a, b, c, d):
            return "('{0}',{1}array({2},bound='{3}'))" .format(a, b, c, d)

        str = ""
        variable_name_index = member.get_dimension_field_index('variableSizeFieldName')
        variable_type_index = member.get_dimension_field_index('variableSizeFieldType')
        size_index = member.get_dimension_field_index('size')
        is_variable_index = member.get_dimension_field_index('isVariableSize')

        if variable_name_index == -1:
            variable_name = "tmpName"
        else:
            variable_name = member.list[variable_name_index].dimension_field_value

        if variable_type_index == -1:
            variable_type = "TNumberOfItems"
        else:
            variable_type = member.list[variable_type_index].dimension_field_value

        str += format_simple_list(variable_name, variable_type)
        str += format_array(member.name, self.lib_imp, member.type, variable_name)

        return str
