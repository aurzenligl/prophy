import os
from xml.dom import minidom


#To jest reader to konkretnych xmlwoych plików a nie genertyczny reader
class XmlReader(object):
    files = []

    def __init__(self, xml_dir_path): # czy oby na pewno ma on czytać pliki w momencie konstrukcji? Potem te dane sa w ramie przez cały czas życia tego obiektu a nie tylko wtedy gdy są potrzebne
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
        return self.tree_files