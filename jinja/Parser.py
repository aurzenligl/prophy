# -*- coding: utf-8 -*-
import options
import re
import sys
from collections import OrderedDict
from data_holder import IncludeHolder,TypeDefHolder,ConstantHolder,EnumHolder,MemberHolder,MessageHolder, DataHolder, UnionHolder


def get_parser():
    path = options.getOptions()[0].in_path
    in_format = options.getOptions()[0].in_format
    print path
    print in_format
    a = {"ISAR": XMLParser(), "SACK": HParser()}
    
    return a[in_format]


class XMLParser(object):

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
        member = MemberHolder(k.attributes["name"].value,k.attributes["type"].value)
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
                    if "bitMaskOr" in value:
                        value = 2
                    elif "EAaMemPoolCid_ApplicationCidStart" in value:
                        value = value.replace("EAaMemPoolCid_ApplicationCidStart",'2')
                    enum.add_to_list(member_enum_element.attributes["name"].value,value)
                dict[name] = enum
        return dict

    def __union_parse(self,tree_node):
        union_list=UnionHolder()
        union_nodes = tree_node.getElementsByTagName('union')
        for union_element in union_nodes:
            union_list.add_to_list(union_element.getAttribute('name'))
        return union_list

    def __typedef_parse(self, tree_node):
        typedef_dict = TypeDefHolder()
        typedef_nodes = tree_node.getElementsByTagName('typedef')
        for typedef_element in typedef_nodes:
            if typedef_element.hasAttribute("type"):
                typedef_dict.add_to_list(typedef_element.attributes["name"].value,typedef_element.attributes["type"].value)
            elif typedef_element.hasAttribute("primitiveType"):
                type = self.__get_type_of_typedef(typedef_element.attributes["primitiveType"].value)
                typedef_dict.add_to_list(typedef_element.attributes["name"].value,type)
        return typedef_dict

    def __get_type_of_typedef(self,value):
        if "8 bit integer unsigned" in value:
            return "u8"
        elif "16 bit integer unsigned" in value:
            return "u16"
        elif "32 bit integer unsigned" in value:
            return "u32"
        elif "64 bit integer unsigned" in value:
            return "u64"
        elif "8 bit integer signed" in value:
            return "i8"
        elif "16 bit integer signed" in value:
            return "i16"
        elif "32 bit integer signed" in value:
            return "i32"
        elif "64 bit integer signed" in value:
            return "i64"
        elif "32 bit float" in value:
            # should be r32 ale nie ma teraz w aprocie obsługi
            return "r32"
        elif "64 bit float" in value:
            # should be r64 ale nie ma teraz w aprocie obsługi
            return "r64"

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

    def parsing_xml_files(self, tree_node):
        data_holder = DataHolder()
        data_holder.constant = self.__constant_parse(tree_node)
        data_holder.typedef = self.__typedef_parse(tree_node)
        data_holder.enum_dict = self.__enum_parse(tree_node)
        data_holder.msgs_list = self.__struct_parse(tree_node, "message")
        data_holder.struct_list = self.__struct_parse(tree_node, "struct")
        data_holder.include = self.__get_include(tree_node)
        data_holder.union = self.__union_parse(tree_node)
        return data_holder

class HParser(object):

    tmp_dict = OrderedDict()
    typedef_dict = {}
    enum_dict = {}
    constant_dict = {}
    class_aprot_string="aprot."

    def __init__(self):
        pass


    def __remove_comments(self, text):
        p = r'/\*[^*]*\*+([^/*][^*]*\*+)*/|("(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\'|.[^/"\'\\]*)'
        return ''.join(m.group(2) for m in re.finditer(p, text, re.M|re.S) if m.group(2))
    
    def __struct_parse(self, file):
        pass

    def __enum_parse(self, file):
        pass

    def __union_parse(self,file):
        pass

    def __typedef_parse(self, file):
        pass

    def __constant_parse(self, file):
        pass

    def __get_include(self, h_file):
        include = IncludeHolder()
        lines = h_file.read()
        
        lines = self.__remove_comments(lines)
        lines = lines.split("\n")
        for line in lines:
            if not line.startswith("//") and not line.startswith("*") and not line.startswith("/*"):
                if "#include" in line:
                    if "<" in line:
                        line = line.split("<")    
                    elif "/" in line:
                        line = line.split("/")
                    else:
                        print "to jest apostrof \""
                        line = line.split('\"')
                                        
                    line = line[-1][:-3]
                    print line
                    include.add_to_list(line)
        return include 

    
    def parsing_h_files(self, h_file):
        data_holder = DataHolder()
        data_holder.include = self.__get_include(h_file)
        