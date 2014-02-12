from jinja2 import Environment, FileSystemLoader, Template
import os
import options
from data_holder_tmp import DataHolder


class TemplateFabric(object):
    def __init__(self):
        self.__template_dir = os.path.join('.', 'templates')

    def get_template(self, template_name):
        env = Environment(loader = FileSystemLoader(self.__template_dir))
        template = env.get_template(template_name)
        return template


class WriterFabric(object):
    @staticmethod
    def get_writer():
        writers = {
            "default": Writer(),
            "python": WriterPython()
             }
        opt = options.getOptions()[0].output
        return writers[opt]


class Writer(object):
    def write_to_file(self, data_holder, template_name, file_name):
        raise NotImplementedError

class WriterPython(Writer): 

    def __init__(self):
        self.__template_fabric = TemplateFabric()

    def write_to_file(self, data_holder, template_name, file_name):
        template = self.__template_fabric.get_template(template_name)
        self.__save_python_file(data_holder, template, file_name)

    def __save_python_file(self, data_holder, template, file_name):
        msg_dict = {}
        typedef = data_holder.typedef.get_list()

        constant = data_holder.constant.get_list()
        enum = data_holder.enum_dict
        print data_holder.msgs_list
        struct_dict = {}

        include_list = data_holder.include.get_list()
        out_folder = "Out_py_files"
        file_dest = os.path.join(out_folder, file_name)
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)
        with open(file_dest+".py", 'w') as f:
            f.write(template.render(msg = msg_dict,
                                    typedef = typedef,
                                    constant = constant,
                                    enum = enum,
                                    struct = struct_dict,
                                    include = include_list))

