import os
from collections import OrderedDict
#from writer import WriterPython
import writer
import options
from data_holder import DataHolder
from reader import XmlReader

class Parser(object):

    tmp_dict = OrderedDict()
    typedef_dict = {}
    enum_dict = {}
    constant_dict = {}
    class_aprot_string="aprot."

    def __struct_parse(self, tree_node, element_name):
        tmp_dict = {}
        struct_dict = {}
        struct_nodes = tree_node.getElementsByTagName(element_name)
        for p in struct_nodes:
            if p.hasChildNodes():
                name = p.attributes["name"].value
                member = p.getElementsByTagName('member')
                for k in member:
                    tmp_dict = self.__checkin_dynamic_fields(k)
                struct_dict[name] = tmp_dict.copy()
                tmp_dict.clear()
        return struct_dict

    def __checkin_dynamic_fields(self, k, dyn_dict=OrderedDict()):
        value = k.attributes["type"].value
        if value.startswith('u'):
            value = self.class_aprot_string + value
        if k.hasChildNodes() and k.getElementsByTagName('dimension'):
            dimension = k.getElementsByTagName('dimension')
            dimension_items={}
            for item ,dim_val in dimension[0].attributes.items():
                if 'Comment' not in item:
                    dimension_items[item]=dim_val
            dyn_dict[k.attributes["name"].value] = dimension_items.copy()
            return dyn_dict
        else:
            dyn_dict[k.attributes["name"].value] = {'type':value}
            return dyn_dict

    def __enum_parse(self, tree_node):
        tmp_dict = {}
        enum_dict = {}
        enum_nodes = tree_node.getElementsByTagName('enum')
        for enum_element in enum_nodes:
            if enum_element.hasChildNodes():
                name = enum_element.attributes["name"].value
                member = enum_element.getElementsByTagName('enum-member')
                for member_enum_element in member:
                    value = member_enum_element.getAttribute('value')
                    tmp_dict[member_enum_element.attributes["name"].value] = value
                enum_dict[name] = tmp_dict.copy()
                tmp_dict.clear()
        return enum_dict

    def __typedef_parse(self, tree_node):
        typedef_dict = {}
        typedef_nodes = tree_node.getElementsByTagName('typedef')
        for typedef_element in typedef_nodes:
            if typedef_element.hasAttribute("type"):
                v=typedef_element.attributes["type"].value
                if v.startswith('T') or v.startswith('S') or v.startswith('U'):
                    typedef_dict[typedef_element.attributes["name"].value] = typedef_element.attributes["type"].value
                else:
                    typedef_dict[typedef_element.attributes["name"].value] = self.class_aprot_string+typedef_element.attributes["type"].value
        return typedef_dict

    def __constant_parse(self, tree_node):
        constant_dict = {}
        constant_nodes = tree_node.getElementsByTagName('constant')
        for constant_element in constant_nodes:
            if constant_element.hasAttribute("value"):
                constant_dict[constant_element.attributes["name"].value]=constant_element.attributes["value"].value
        return constant_dict

    def __get_include(self, tree_node):
            include_list = []
            include_nodes = tree_node.getElementsByTagName("xi:include")
            for include_element in include_nodes:
                if include_element.hasAttribute("href"):
                    x=include_element.attributes["href"].value
                    x=x.partition('.')[0]
                    include_list.append(x)
            return include_list

    def parsing_xml_files(self, tree_node,data_holder):
        data_holder.constant_dict=self.__constant_parse(tree_node)
        data_holder.typedef_dict=self.__typedef_parse(tree_node)
        data_holder.enum_dict=self.__enum_parse(tree_node)
        data_holder.msg_dict=self.__struct_parse(tree_node, "message")
        data_holder.struct_dict=self.__struct_parse(tree_node, "struct")
        data_holder.include_list=self.__get_include(tree_node)
        return data_holder

if __name__ == "__main__":
    options, args = options.getOptions()
    xml_path = options.isar_path
    reader = XmlReader(xml_path)
    parser = Parser()
    writer = writer.WriterFabric.get_writer()
    data_holder = DataHolder()
    reader.read_files()
    tree_files = reader.return_tree_files()
    template_name = "temp.txt"
    dict={}
    for file_name,tree_node in tree_files.iteritems():
         data_holder = parser.parsing_xml_files(tree_node,data_holder)
         writer.write_to_file(data_holder,template_name,file_name)
    print dict
