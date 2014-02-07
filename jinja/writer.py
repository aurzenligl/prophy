from jinja2 import Environment, FileSystemLoader, Template
import os
import data_holder


class Writer(object):

    def write_py_file(self, data_holder, script_dir, template_name, file_name):
        self.data_holder = data_holder
        template = self.__set_template(script_dir, template_name)
        self.__save_python_file(file_name, template)

    def __save_python_file(self, file_name, template,data_holder):
        msg_dict, typedef_dict, constant_dict, enum_dict, struct_dict = data_holder.return_dicts()
        with open(file_name+".py", 'w') as f:
            f.write(template.render(msg=msg_dict,
                                    type=typedef_dict,
                                    const=constant_dict,
                                    enum=enum_dict,
                                    struct=struct_dict))

    def __set_template(script_dir, template_name):
        template_dir = os.path.join(script_dir, 'template')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        return template