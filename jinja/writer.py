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



class WriterFabric(object):
    @staticmethod
    def get_writer(directory,file_name, writer = "txt"):
        mode = WriterFabric.__get_mode()
        return WriterTxt(directory,file_name, mode)

    @staticmethod
    def __get_mode():
        return "w"

class WriterTxt(object):
    def __init__(self,directory, file_name, mode):
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_dest=os.path.join(directory, file_name)
        self.__file_h = open(file_dest, mode)

    def write_to_file(self, tekst):
        self.__file_h.write(tekst)
