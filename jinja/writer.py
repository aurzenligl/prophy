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
        out += self._serialize_constant(dataHolder.constant.get_list()) + os.linesep
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
            if val.startswith('u') or val.startswith('i'):
                out += key + " = " + self.lib_imp + val + '\n'
            else:
                out += key + " = "  + val + '\n'
        return out

    def _serialize_include(self, include_list):
        out = ""
        for inc in include_list:
            out += "from " + inc + " import *" + '\n'
        return out

    def _serialize_constant(self, constant_list):
        out = ""
        for key, val in constant_list:
            out += key + " = " +val+ '\n'
        return out

    def _serialize_msgs(self,msgs_list):
        out = ""
        lib_imp = self.lib_imp
        for key in msgs_list:
            out += "class {0}({1}struct):" .format(key.name,self.lib_imp) + "\n"
            out += "    __metaclass__ = aprot.struct_generator" + "\n"
            out += "    _descriptor = ["
            desc = []
            for member in key.get_list():
                if member.type.startswith('u') or member.type.startswith('i'):
                    lib_imp = self.lib_imp
                else :
                    lib_imp = ""
                if len(member.list) > 0:
                    out += self._serialize_msg_member(member,lib_imp)
                else:
                    desc.append("('{0}',{1}{2})" .format(member.name ,lib_imp, member.type))
            out += ", ".join(desc)
            out += "]"
            out += "\n"
        return out

    def _serialize_msg_member(self,member,lib_imp):
        str = ""
        if not "isVariableSize" in member.list:
            str += "('{0}',{1}{2})" .format(member.name ,lib_imp, member.type) + os.linesep + "\n\t\t\t\t   "
        return str


class WriterFabric(object):
    @staticmethod
    def get_writer(file_name, writer = "txt", mode = "w+"):
        return WriterTxt(file_name, mode)

class WriterTxt(object):
    def __init__(self, file_name, mode):
        self.__file_h = open(file_name, mode)

    def write_to_file(self, tekst):
        self.__file_h.write(tekst)
