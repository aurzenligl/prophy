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
    def serialize(self, dataHolder):
        return self.__serialize_enum(dataHolder.enum_dict) + os.linesep

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
            if val.startswith('u'):
                out += key +" = "+val+ os.linesep
            else:
                out += key +" = "+"aprot."+val+ os.linesep
        return out

    def _serialize_include(self, include_list):
        out = ""
        for inc in include_list:
            out += "from " + inc + " import *" + os.linesep
        return out



class WriterFabric(object):
    @staticmethod
    def get_writer(file_name, writer = "txt", mode = "w+"):
        return WriterTxt(file_name, mode)

class WriterTxt(object):
    def __init__(self, file_name, mode):
        self.__file_h = open(file_name, mode)

    def write_to_file(self, tekst):
        self.__file_h.write(tekst)
