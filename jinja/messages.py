import os
from collections import OrderedDict
import writer

import options
from reader import XmlReader
from Parser import Parser


if __name__ == "__main__":
    options, args = options.getOptions()
    xml_path = options.isar_path
    reader = XmlReader(xml_path)
    parser = Parser()

    reader.read_files()
    tree_files = reader.return_tree_files()
    template_name = "temp.txt"
    directory_dst = options.out_path
    for file_name,tree_node in tree_files.iteritems():
          data_holder = parser.parsing_xml_files(tree_node)
          w=writer.WriterTxt(directory_dst,file_name+".py","w")
          ps = writer.PythonSerializer()
          o = ps.serialize(data_holder)
          w.write_to_file(o)

