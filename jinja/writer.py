from jinja2 import Environment, FileSystemLoader, Template
import os
from data_holder import DataHolder

class Writer(object):

    def write_py_file(self,data_holder,template_name, file_name):
        template = self.__set_template(template_name)
        self.__save_python_file(data_holder,template,file_name)

    def __save_python_file(self,data_holder,template,file_name):
        msg_dict=data_holder.get_msg_dict()
        typedef_dict=data_holder.get_typedef_dict()
        constant_dict=data_holder.get_constant_dict()
        enum_dict=data_holder.get_enum_dict()
        struct_dict=data_holder.get_struct_dict()
        include_dict=data_holder.get_include_dict()
        out_folder="Out_py_files"
        file_dest=os.path.join(out_folder,file_name)
        if not os.path.exists(out_folder):
            os.mkdir(out_folder)
        with open(file_dest+".py", 'w') as f:
            f.write(template.render(msg=msg_dict,
                                    typedef=typedef_dict,
                                    constant=constant_dict,
                                    enum=enum_dict,
                                    struct=struct_dict,
                                    include=include_dict))

    def __set_template(self,template_name):
        template_dir = os.path.join('.', 'templates')
        print template_dir
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        return template