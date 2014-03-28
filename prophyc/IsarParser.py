# -*- coding: utf-8 -*-

import xml.dom.minidom
import model

def _get_struct_name_and_index(struct_list, struct_dict):
    for x in struct_list:
        index = struct_list.index(x)
        struct_dict[x.name] = index

def _sorter(struct_list, index, out_list, struct_dict, lista):
    element = struct_list[index]
    element_name = element.name
    for member_elem in element.members:
        member_type = member_elem.type
        if member_type.startswith('S') and member_type in struct_dict:
            index = struct_dict[member_type]
            x = struct_list[index]
            if x not in out_list:
                out_list.extend(_sorter(struct_list, index, out_list, struct_dict, lista))
        else:
            for x in struct_list:
                if member_type in x.name:
                    if x not in out_list:
                        out_list.append(x)
    if element not in out_list:
        out_list.append(element)
    return lista

def sort_struct(struct_list):
    index = 0
    out_list = []
    struct_dict = {}
    lista = []
    _get_struct_name_and_index(struct_list, struct_dict)
    for struct_elem_index in xrange(len(struct_list)):
        out_list.extend(_sorter(struct_list, struct_elem_index, out_list, struct_dict, lista))
    return out_list

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

    def __struct_parse(self, tree_node, element_name):
        list = []
        struct_nodes = tree_node.getElementsByTagName(element_name)
        for p in struct_nodes:
            if p.hasChildNodes():
                msg = model.Struct()
                msg.name = p.attributes["name"].value
                member = p.getElementsByTagName('member')
                for k in member:
                    msg.members.extend(self.__checkin_member_fields(k))
                list.append(msg)
        return list

    def __checkin_member_fields(self, k):
        members = []
        kname = k.attributes["name"].value
        ktype = k.attributes["type"].value
        if k.hasChildNodes() and k.getElementsByTagName('dimension'):
            dimension = k.getElementsByTagName('dimension')
            dimension_tags = dict(dimension[0].attributes.items())

            if "isVariableSize" in dimension_tags:
                if "variableSizeFieldType" in dimension_tags:
                    type = dimension_tags["variableSizeFieldType"]
                else:
                    type = "u32"
                if "variableSizeFieldName" in dimension_tags:
                    name = dimension_tags["variableSizeFieldName"]
                else:
                    name = kname + "_len"
                members.append(model.Struct.Member(name, type, None, None, None))
                members.append(model.Struct.Member(kname, ktype, True, name, None))
            elif "size" in dimension_tags:
                members.append(model.Struct.Member(kname, ktype, True, None, dimension_tags["size"]))
        else:
            members.append(model.Struct.Member(kname, ktype, None, None, None))
        return members

    def __get_enum_member(self, elem):
        value = elem.getAttribute('value')
        value = value if value != "-1" else "0xFFFFFFFF"
        return (elem.attributes["name"].value, value)

    def __get_enum(self, elem):
        if not elem.hasChildNodes():
            return None
        name = elem.attributes["name"].value
        enumerators = [self.__get_enum_member(member) for member in elem.getElementsByTagName('enum-member')]
        return (name, enumerators)

    def __get_enums(self, dom):
        return dict(filter(None, (self.__get_enum(elem) for elem in dom.getElementsByTagName('enum'))))

    def __union_parse(self, tree_node):
        union_dict = {}
        enum_dict = {}

        union_nodes = tree_node.getElementsByTagName('union')
        for union_element in union_nodes:
            name = union_element.getAttribute('name')
            union = DataHolder.UnionHolder()
            enum = []
            member = union_element.getElementsByTagName("member")
            for member_union_element in member:
                discriminatorValue = member_union_element.getAttribute('discriminatorValue')
                member_type = member_union_element.getAttribute('type')
                member_name = member_union_element.getAttribute('name')
                union.add_to_list(member_type, member_name)
                enum.append(("EDisc" + name + "_" + member_name + "_" + discriminatorValue, discriminatorValue))
            union_dict[name] = union
            enum_dict["EDisc" + name] = enum
        return union_dict, enum_dict

    def __get_typedef(self, elem):
        if elem.hasAttribute("type"):
            return (elem.attributes["name"].value, elem.attributes["type"].value)
        elif elem.hasAttribute("primitiveType"):
            type = self.primitive_types[elem.attributes["primitiveType"].value]
            return ((elem.attributes["name"].value, type))

    def __get_typedefs(self, dom):
        return filter(None, (self.__get_typedef(elem) for elem in dom.getElementsByTagName('typedef')))

    def __sort_constants(self, list):
        primitive = filter(lambda constant: constant[1].isdigit(), list)
        complex = filter(lambda constant: not constant[1].isdigit(), list)
        return primitive + complex

    def __get_constant(self, elem):
        return (elem.attributes["name"].value, elem.attributes["value"].value)

    def __get_constants(self, dom):
        return self.__sort_constants([self.__get_constant(elem) for elem in dom.getElementsByTagName('constant')])

    def __get_includes(self, dom):
        return [elem.attributes["href"].value.split('.')[0] for elem in dom.getElementsByTagName("xi:include")]

    def __parse_tree_node(self, tree_node):
        data_holder = model.DataHolder()
        data_holder.constants = self.__get_constants(tree_node)
        data_holder.typedefs = self.__get_typedefs(tree_node)
        data_holder.enums = self.__get_enums(tree_node).items()
        data_holder.structs = sort_struct(self.__struct_parse(tree_node, "struct"))
        data_holder.structs += self.__struct_parse(tree_node, "message")
        data_holder.includes = self.__get_includes(tree_node)
        data_holder.union_dict, temp_dict = self.__union_parse(tree_node)
        data_holder.enums += temp_dict.items()
        return data_holder

    def parse_string(self, string):
        return self.__parse_tree_node(xml.dom.minidom.parseString(string))

    def parse(self, file):
        return self.__parse_tree_node(xml.dom.minidom.parse(file))
