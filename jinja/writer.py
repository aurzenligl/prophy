from jinja2 import Environment, FileSystemLoader, Template
import os
import options
from data_holder import DataHolder

class TemplateFabric(object):
    def __init__(self):
        self.__template_dir = os.path.join('.', 'templates')

    def get_template(self, template_name):
        env = Environment(loader = FileSystemLoader(self.__template_dir))
        template = env.get_template(template_name)
        return template

class PythonSerializer(object):
    def __init__(self):
        self.lib_imp="aprot."

    def serialize(self, dataHolder):
        out = ""
        out += self._serialize_include(dataHolder.include.get_list()) + os.linesep
        out += self._serialize_constant(dataHolder.constant) + os.linesep
        out += self._serialize_typedef(dataHolder.typedef.get_list()) + os.linesep
        out += self._serialize_enum(dataHolder.enum_dict) + os.linesep
        out += self._serialize_msgs(dataHolder.struct_list)
        out += self._serialize_msgs(dataHolder.msgs_list)
        return out

    def _serialize_enum(self, enum_dic):
        template = TemplateFabric().get_template("enum.txt");
        out = ""
        for key, val in enum_dic.iteritems():
            out += template.render(key = key, value = val.list)
            out += os.linesep
        return out

    def _serialize_typedef(self, typedef_list):
        out = ""
        for key, val in typedef_list:
            if val.startswith('u') or val.startswith('i') or val.startswith('r'):
                out += key + " = " + self.lib_imp + val + '\n'
            else:
                out += key + " = "  + val + '\n'
        return out

    def _serialize_include(self, include_list):
        out = "import aprot \n"
        for inc in include_list:
            out += "from " + inc + " import *" + '\n'
        return out

    def _serialize_constant(self, constant):
        out = ""
        for key,val in constant.get_sorted_list():
            out += key + " = " + val + '\n'
        return out

    def _serialize_msgs(self,msgs_list):
        out = ""

        def serialize_members(keys):
            lib_imp = self.lib_imp
            desc = []
            for member in keys:
                if member.type.startswith('u') or member.type.startswith('i') or member.type.startswith('r')  :
                    lib_imp = self.lib_imp
                else :
                    lib_imp = ""
                if len(member.list) > 0:
                    desc.append(self._serialize_msg_member(member))
                else:
                    desc.append("('{0}',{1}{2})" .format(member.name ,lib_imp, member.type))
            return ", ".join(desc)
        for key in msgs_list:
            out += "class {0}({1}struct):" .format(key.name, self.lib_imp) + "\n"
            out += "    __metaclass__ = aprot.struct_generator" + "\n"
            out += "    _descriptor = [" + serialize_members(key.get_list()) + "]\n"
        return out

    def _serialize_msg_member(self, member):
        str = ""
        variable_name_index = member.get_dimension_field_index('variableSizeFieldName')
        variable_type_index = member.get_dimension_field_index('variableSizeFieldType')
        size_index = member.get_dimension_field_index('size')
        min_size_index = member.get_dimension_field_index('minSize')
        is_variable_index = member.get_dimension_field_index('isVariableSize')

        if len(member.list) == 4 and variable_name_index != -1 and variable_type_index != -1 :
            str += "('{0}',{1}), " .format(member.list[variable_name_index].dimension_field_value, member.list[variable_type_index].dimension_field_value)
            str += "('{0}',{1}array({2},bound='{3}'))" .format(member.name, self.lib_imp, member.type, member.list[variable_name_index].dimension_field_value)
        if len(member.list) == 5:
            str += "('{0}',{1}), " .format(member.list[variable_name_index].dimension_field_value, member.list[variable_type_index].dimension_field_value)
            str += "('{0}',{1}array({2},bound='{3}'))" .format(member.name, self.lib_imp, member.type, member.list[variable_name_index].dimension_field_value)
        if  variable_type_index == -1 and variable_name_index != -1:
            str += "('{0}',{1}), " .format(member.list[variable_name_index].dimension_field_value,'TNumberOfItems')
            str += "('{0}',{1}array({2},bound='{3}'))" .format(member.name, self.lib_imp, member.type, member.list[variable_name_index].dimension_field_value)
        if variable_name_index == -1 and variable_type_index != -1:
            str += "('{0}',{1}), " .format('tmpName', member.list[variable_type_index].dimension_field_value)
            str += "('{0}',{1}array({2},bound='{3}'))" .format(member.name, self.lib_imp, member.type,'tmpName')
        if variable_name_index == -1 and variable_type_index == -1:
            str += "\" variable_name_index == -1 and variable_type_index == -1\""
        if len(member.list) == 3 and variable_name_index == -1 and variable_type_index == -1 and size_index != -1 and min_size_index != -1:
            str += "('{0}',{1}), " .format('tmpName','TNumberOfItems')
            str += "('{0}',{1}array({2},bound='{3}'))" .format(member.name, self.lib_imp, member.type,'tmpName')
        if len(member.list) == 2 and size_index != -1 and is_variable_index != -1:
            str += "('{0}',{1}), " .format('tmpName','TNumberOfItems')
            str += "('{0}',{1}array({2},bound='{3}'))" .format(member.name, self.lib_imp, member.type,'tmpName')
        if len(member.list) == 1 and size_index != -1:
            str += "('{0}',{1}), " .format('tmpName','TNumberOfItems')
            str += "('{0}',{1}array({2},bound='{3}'))" .format(member.name, self.lib_imp, member.type,'tmpName')

        return str


class WriterFabric(object):
    @staticmethod
    def get_writer(directory,file_name, writer = "txt", mode = "w+"):
        return WriterTxt(directory,file_name, mode)

class WriterTxt(object):
    def __init__(self,directory, file_name, mode):
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_dest=os.path.join(directory, file_name)
        self.__file_h = open(file_dest, mode)

    def write_to_file(self, tekst):
        self.__file_h.write(tekst)
