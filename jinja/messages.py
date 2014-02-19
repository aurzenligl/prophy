import writer
import Serializers
import options
import reader
import Parser

if __name__ == "__main__":
    options, args = options.getOptions()
    reader = reader.get_reader()
    parser = Parser.get_parser()

    reader.read_files()
    tree_files = reader.return_tree_files()
    template_name = "temp.txt"
    for file_name,tree_node in tree_files.iteritems():
          data_holder = parser.parsing_xml_files(tree_node)
          w = writer.get_writer(file_name+".py")
          ps = Serializers.get_serializer()
          o = ps.serialize(data_holder)
          w.write_to_file(o)

