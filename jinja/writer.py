from jinja2 import Environment, FileSystemLoader,Template
import os

class writer(object):

    def write_py_file(self,msg_dict,typedef_dict,enum_dict,struct_dict,file_name,script_dir,template_name):
        self.__set_dicts(msg_dict,typedef_dict,enum_dict,struct_dict)
        template=self.__set_template(script_dir,template_name)
        self.__

    def __save_python_file(self,file_name,template):
        with open(file_name+".py", 'w') as f:
            f.write(template.render())

    def __set_template(script_dir,template_name):
        template_dir=os.path.join(script_dir, 'template')
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_name)
        return template