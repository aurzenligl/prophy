import os
from xml.dom import minidom
import options
import collections

def get_reader():
    path = options.getOptions()[0].in_path
    in_format = options.getOptions()[0].in_format
    print path
    print in_format
    a = {"ISAR": XmlReader(path), "SACK": HReader(path)}
    
    return a[in_format]

class HReader(object):

    def __init__(self, sack_dir_path):
        self.dirs = []
        self.files = collections.OrderedDict()   #dict files key file_name, value path
        self.__get_files_and_dict(sack_dir_path)

    def __get_files_and_dict(self, path):
        for root, dirs, files in os.walk(path):
            if len(dirs) != 0:
                for d in dirs:
                    self.dirs.append(os.path.join(root, d))
            if len(files) != 0:
                for f in files:
                    if f.endswith(".h"):
                        self.files[f[:-2]] = os.path.join(root, f)  

    def open_file(self, file_path):
        with open(file_path, "r") as f:
            return f

    def get_structure(self):
        return self.dirs

    def get_files(self):
        return self.files

class XmlReader(object):
    files = []

    def __init__(self, xml_dir_path):
        self.tree_files = {}
        self.xml_dir = xml_dir_path

    def __open_files(self):
        for x in self.files:
            self.tree_files[x.partition('.')[0]]=self.__open_file(x)

    def __open_file(self, file):
        file_dir = os.path.join(self.xml_dir, file)
        dom_tree = minidom.parse(file_dir)
        return dom_tree

    def __set_files_to_parse(self):
        all_files = os.listdir(self.xml_dir)
        for f in all_files:    # TODO: Think about some error message, now I do not know whether the operation was successful - see the first test
            if f.endswith('.xml'):
                self.files.append(f)

    def read_files(self):
        self.__set_files_to_parse()
        self.__open_files()

    def return_tree_files(self):
        if len(self.tree_files.keys()) == 0:
            self.read_files()
        return self.tree_files
