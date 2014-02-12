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
        return self.__serialize_enum(dataHolder.dic["enum"]) + os.linesep

    def __serialize_enum(self, enum_data_holder):
        template = TemplateFabric().get_template("enum.txt");
        template.render(key = enum_data_holder.get_enum_holder_name, value = enum_data_holder.get_list_values())



class WriterFabric(object):
    @staticmethod
    def get_writer(file_name, writer = "txt", mode = "w+"):
        return WriterTxt(file_name, mode)

class WriterTxt(object):
    def __init__(self, file_name, mode):
        self.__file_h = open(file_name, mode)

    def write_to_file(self, tekst):
        self.__file_h.write(tekst)
