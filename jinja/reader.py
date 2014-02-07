import os
from xml.dom import minidom


class Reader(object):

    files = []

    def __init__(self, xml_dir_path):
        self.tree_files = []
        self.xml_dir = xml_dir_path
        self.script_dir = os.path.dirname(os.path.realpath(__file__))   # FIXME: What is this variable?
        self.__set_files_to_parse()
        self.__open_files()

    def __open_files(self):
        for x in self.files:
            self.tree_files.append(self.__open_file(x))

    def __open_file(self, file):
        file_dir = os.path.join(self.xml_dir, file)
        dom_tree = minidom.parse(file_dir)
        return dom_tree

    def __set_files_to_parse(self):
        all_files = os.listdir(self.xml_dir)
        for f in all_files:    # TODO: Think about some error message, now I do not know whether the operation was successful - see the first test
            if f.endswith('.xml'):
                self.files.append(f)

    def return_tree_files(self):
        return self.tree_files