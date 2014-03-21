import os
import options
import sys
from data_holder import DataHolder

class TemplateFabric(object):
    def __init__(self):
        self.__template_dir = os.path.join('.', 'templates')

    def get_template(self, template_name):
        env = Environment(loader = FileSystemLoader(self.__template_dir))
        template = env.get_template(template_name)
        return template

def get_writer(file_name):
    mode = "w"
    directory = options.getOptions()[0].out_path
    return  WriterTxt(directory, file_name, mode)

class WriterTxt(object):
    def __init__(self, directory, file_name, mode):
        if not os.path.exists(directory):
            os.makedirs(directory)
        open(os.path.join(directory,'__init__.py'),'w').close()
        sys.path.append(directory)
            
        file_dest = os.path.join(directory, file_name)
        self.__file_h = open(file_dest, mode)

    def write_to_file(self, tekst):
        self.__file_h.write(tekst)

class MakeStructure(object):
    def __init__(self, dirs):
        out_path = options.getOptions()[0].out_path
        in_path = options.getOptions()[0].in_path
        for element in dirs:
            element = element.replace(in_path, out_path)
            if not os.path.exists(element):
                os.makedirs(element)

class WriteID(object):
    def __init__(self):
        directory = options.getOptions()[0].out_path
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        file_dest = os.path.join(directory, 'MessageId_Lte.py')
        self.__file_h = open(file_dest, 'w')

    def write_to_file(self, ids_obj):
        self.__file_h.write("import prophy\n\n")
        for k,v in ids_obj.ids_dict.iteritems():
            self.__file_h.write(k + " " + v + "\n")
