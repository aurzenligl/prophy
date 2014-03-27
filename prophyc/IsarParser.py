# -*- coding: utf-8 -*-

import xml.dom.minidom
from collections import OrderedDict
from DataHolder import ConstantHolder, EnumHolder, MemberHolder, MessageHolder, DataHolder, UnionHolder

class IsarParser(object):

    primitive_types = {"8 bit integer unsigned": "u8",
                       "16 bit integer unsigned": "u16",
                       "32 bit integer unsigned": "u32",
                       "64 bit integer unsigned": "u64",
                       "8 bit integer signed": "i8",
                       "16 bit integer signed": "i16",
                       "32 bit integer signed": "i32",
                       "64 bit integer signed": "i64",
                       "32 bit float": "r32",
                       "64 bit float": "r64"}

    tmp_dict = OrderedDict()
    typedef_dict = {}
    enum_dict = {}
    constant_dict = {}
    class_aprot_string = "aprot."

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
        member = MemberHolder(k.attributes["name"].value, k.attributes["type"].value)
        if k.hasChildNodes() and k.getElementsByTagName('dimension'):
            dimension = k.getElementsByTagName('dimension')
            for item , dim_val in dimension[0].attributes.items():
                if 'Comment' not in item:
                    member.add_to_list(item, dim_val)
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
                        value = value.replace("EAaMemPoolCid_ApplicationCidStart", '2')
                    enum.add_to_list(member_enum_element.attributes["name"].value, value)
                dict[name] = enum
        return dict

    def __union_parse(self, tree_node):
        union_dict = {}
        enum_dict = {}

        union_nodes = tree_node.getElementsByTagName('union')
        for union_element in union_nodes:
            name = union_element.getAttribute('name')
            union = UnionHolder()
            enum = EnumHolder()
            member = union_element.getElementsByTagName("member")
            for member_union_element in member:
                discriminatorValue = member_union_element.getAttribute('discriminatorValue')
                member_type = member_union_element.getAttribute('type')
                member_name = member_union_element.getAttribute('name')
                union.add_to_list(member_type, member_name)
                enum.add_to_list("EDisc" + name + "_" + member_name + "_" + discriminatorValue, discriminatorValue)
            union_dict[name] = union
            enum_dict["EDisc" + name] = enum
        return union_dict, enum_dict

    def __get_typedef(self, elem):
        if elem.hasAttribute("type"):
            return (elem.attributes["name"].value, elem.attributes["type"].value)
        elif elem.hasAttribute("primitiveType"):
            type = self.primitive_types[elem.attributes["primitiveType"].value]
            return ((elem.attributes["name"].value, type))
        else:
            raise Exception("Typedef has no type nor primitiveType attribute")

    def __get_typedefs(self, dom):
        return [self.__get_typedef(elem) for elem in dom.getElementsByTagName('typedef')]

    def __constant_parse(self, tree_node):
        constant = ConstantHolder()
        constant_nodes = tree_node.getElementsByTagName('constant')
        for constant_element in constant_nodes:
            if constant_element.hasAttribute("value"):
                constant.add_to_list(constant_element.attributes["name"].value, constant_element.attributes["value"].value)
        return constant

    def __get_includes(self, dom):
        return [elem.attributes["href"].value.split('.')[0] for elem in dom.getElementsByTagName("xi:include")]

    def __parse_tree_node(self, tree_node):
        temp_dict = {}
        data_holder = DataHolder()
        data_holder.constant = self.__constant_parse(tree_node)
        data_holder.typedefs = self.__get_typedefs(tree_node)
        data_holder.enum_dict = self.__enum_parse(tree_node)
        data_holder.msgs_list = self.__struct_parse(tree_node, "message")
        data_holder.struct_list = self.__struct_parse(tree_node, "struct")
        data_holder.includes = self.__get_includes(tree_node)
        data_holder.union_dict, temp_dict = self.__union_parse(tree_node)
        data_holder.enum_dict = dict(data_holder.enum_dict.items() + temp_dict.items())
        return data_holder

    def parse_string(self, string):
        return self.__parse_tree_node(xml.dom.minidom.parseString(string))

    def parse(self, file):
        return self.__parse_tree_node(xml.dom.minidom.parse(file))
