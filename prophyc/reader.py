import os
from xml.dom import minidom
import options
import collections

def get_reader():
    path = options.getOptions()[0].in_path
    in_format = options.getOptions()[0].in_format
    a = {"ISAR": XmlReader(path), "SACK": HReader(path)}

    return a[in_format]

class HReader(object):

    def __init__(self, sack_dir_path):
        self.dirs = []
        self.files = collections.OrderedDict()  # dict files key file_name, value path
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
        try:
            f = open(file_path, "r")
            return f
        except IOError:
            print "Could not open file!"

    def get_structure(self):
        return self.dirs

    def get_files(self):
        return self.files

class XmlReader(object):
    def __init__(self, filename):
        self.filename = filename
        self.basename = os.path.splitext(filename)[0]
        self.xml_tree = minidom.parse(filename)
