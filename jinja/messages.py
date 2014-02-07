import os
from collections import OrderedDict
import writer
import options
from data_holder import DataHolder
#FIME: Turn ON "show whitespace" in IDE, and fix all spaces to tabs. If interpreter got an error in indentation you'll never find it.
# In LOM we use spaces insed of tabs


class Parser(object):

    tmp_dict = OrderedDict()
    typedef_dict = {}
    enum_dict = {}
    constant_dict = {}

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
            value = "aprot." + value
        if k.hasChildNodes() and k.getElementsByTagName('dimension'):
            dimension = k.getElementsByTagName('dimension')
            if dimension[0].hasAttribute('size') and not dimension[0].hasAttribute('isVariableSize'):
                dyn_dict[k.attributes["name"].value] = (value, dimension[0].attributes['size'].value)
            elif dimension[0].hasAttribute('isVariableSize'):
                if dimension[0].hasAttribute('variableSizeFieldType') and dimension[0].hasAttribute('variableSizeFieldName'):
                    dyn_dict[k.attributes["name"].value] = (value, dimension[0].attributes['size'].value,
                                                            dimension[0].attributes['variableSizeFieldType'].value,
                                                            dimension[0].attributes['variableSizeFieldName'].value)
                elif dimension[0].hasAttribute('variableSizeFieldType') and not dimension[0].hasAttribute('variableSizeFieldName'):
                    dyn_dict[k.attributes["name"].value] = (value, dimension[0].attributes['size'].value,
                                                            dimension[0].attributes['variableSizeFieldType'].value, "blabla ba")
                elif dimension[0].hasAttribute('variableSizeFieldName') and not dimension[0].hasAttribute('variableSizeFieldType'):
                    dyn_dict[k.attributes["name"].value] = (value, dimension[0].attributes['size'].value,
                                                            'TNumberOfItems',
                                                            dimension[0].attributes['variableSizeFieldName'].value)
        else:
            dyn_dict[k.attributes["name"].value] = (value)
        return dyn_dict

    def __enum_parse(self, tree_node):
        tmp_dict = {}
        enum_dict = {}
        enum_nodes = tree_node.getElementsByTagName('enum')
        for enum_element in enum_nodes:
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
                typedef_dict[typedef_element.attributes["name"].value] = typedef_element.attributes["type"].value
        return typedef_dict

    def __constant_parse(self, tree_node):
        constant_dict = {}
        constant_nodes = tree_node.getElementsByTagName('constant')
        for constant_element in constant_nodes:
            if constant_element.hasAttribute("value"):
                constant_dict[constant_element.attributes["name"].value]=constant_element.attributes["value"].value
        return constant_dict

    def __get_include(self, tree_node):
            include_dict = {}
            include_nodes = tree_node.getElementsByTagName("xi:include")
            for include_element in include_nodes:
                if include_element.hasAttribute("href"):
                    include_dict[include_element.attributes["href"].value] = include_element.attributes["xpath"].value
            return include_dict

    def parsing_xml_files(self, tree_files):
        #data_holder = DataHolder()
        #const_dict, typedef_dict = {}
        for tree_node in tree_files:
            self.__constant_parse(tree_node)
            self.__typedef_parse(tree_node)
            self.__enum_parse(tree_node)
            self.__struct_parse(tree_node, "message")
            self.__struct_parse(tree_node, "struct")
            self.__get_include(tree_node)
            #data_holder.set_dicts()

if __name__ == "__main__":
    #xml_path = options.isar_path
    #parser = Parser(xml_path)
    #options, args = options.getOptions()
    #parser.parsing_xml_files()