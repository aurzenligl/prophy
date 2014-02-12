import os
from collections import OrderedDict
import options
from data_holder import DataHolder
from reader import XmlReader
from data_holder import IncludeHolder,TypeDefHolder,ConstantHolder,EnumHolder,MemberHolder,MessageHolder

class Parser(object):

    tmp_dict = OrderedDict()
    typedef_dict = {}
    enum_dict = {}
    constant_dict = {}
    class_aprot_string="aprot."

    def __struct_parse(self, tree_node, element_name):
        list = []
        struct_nodes = tree_node.getElementsByTagName(element_name)
        for p in struct_nodes:
            if p.hasChildNodes():
                msg = MessageHolder()
                msg.name = p.attributes["name"].value
                member = p.getElementsByTagName('member')
                for k in member:
                    msg.add_to_list(self.__checkin_member_fields(k))
                list.append(msg)
        return list

    def __checkin_member_fields(self, k):
        member = MemberHolder()
        value = k.attributes["type"].value
        member.name = k.attributes["name"].value
        member.type = value
        if k.hasChildNodes() and k.getElementsByTagName('dimension'):
            dimension = k.getElementsByTagName('dimension')
            for item ,dim_val in dimension[0].attributes.items():
                if 'Comment' not in item:
                    member.add_to_list(item,dim_val)
        return member

    def __enum_parse(self, tree_node):
        dict = {}
        enum_nodes = tree_node.getElementsByTagName('enum')
        for enum_element in enum_nodes:
            if enum_element.hasChildNodes():

                name = enum_element.attributes["name"].value
                enum = EnumHolder()
                member = enum_element.getElementsByTagName('enum-member')
                for member_enum_element in member:
                    value = member_enum_element.getAttribute('value')
                    enum.add_to_list(member_enum_element.attributes["name"].value,value)
                dict[name] = enum.get_list()
        return dict

    def __typedef_parse(self, tree_node):
        typedef_dict = TypeDefHolder()
        typedef_nodes = tree_node.getElementsByTagName('typedef')
        for typedef_element in typedef_nodes:
            if typedef_element.hasAttribute("type"):
                typedef_dict.add_to_list(typedef_element.attributes["name"].value,typedef_element.attributes["type"].value)
        return typedef_dict

    def __constant_parse(self, tree_node):
        constant=ConstantHolder()
        constant_nodes = tree_node.getElementsByTagName('constant')
        for constant_element in constant_nodes:
            if constant_element.hasAttribute("value"):
                constant.add_to_list(constant_element.attributes["name"].value,constant_element.attributes["value"].value)
        return constant

    def __get_include(self, tree_node):
            include = IncludeHolder()
            include_nodes = tree_node.getElementsByTagName("xi:include")
            for include_element in include_nodes:
                if include_element.hasAttribute("href"):
                    x = include_element.attributes["href"].value
                    x = x.partition('.')[0]
                    include.add_to_list(x)
            return include

    def parsing_xml_files(self, tree_node,data_holder):
        data_holder.constant = self.__constant_parse(tree_node)
        data_holder.typedef = self.__typedef_parse(tree_node)
        data_holder.enum_dict = self.__enum_parse(tree_node)
        data_holder.msgs_lists = self.__struct_parse(tree_node, "message")
        data_holder.struct_dict = self.__struct_parse(tree_node, "struct")
        data_holder.include = self.__get_include(tree_node)
        return data_holder

if __name__ == "__main__":
    options, args = options.getOptions()
    xml_path = options.isar_path
    reader = XmlReader(xml_path)
    parser = Parser()
    writer = writer_cop.WriterFabric.get_writer()
    data_holder = DataHolder()
    reader.read_files()
    tree_files = reader.return_tree_files()
    template_name = "temp.txt"
    dict = {}
    for file_name,tree_node in tree_files.iteritems():
         data_holder = parser.parsing_xml_files(tree_node,data_holder)
         writer.write_to_file(data_holder,template_name,file_name)
    print dict
