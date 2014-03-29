# -*- coding: utf-8 -*-

import xml.dom.minidom
import model
from itertools import ifilter, islice

def get_typedef_deps(typedef):
    return [typedef.type]

def get_enum_deps(enum):
    return []

def get_struct_deps(struct):
    return [member.type for member in struct.members]

deps_visitor = {model.Typedef: get_typedef_deps,
                model.Enum: get_enum_deps,
                model.Struct: get_struct_deps}

def get_deps(node):
    return deps_visitor[type(node)](node)

def dependency_sort(nodes):
    known = set()
    index = 0
    max_index = len(nodes)

    while index < max_index:
        node = nodes[index]
        for dep in get_deps(node):
            if dep not in known:
                found = next(ifilter(lambda x: x.name == dep, islice(nodes, index, None)), None)
                if found:
                    found_index = nodes.index(found)
                    nodes.insert(index, nodes.pop(found_index))
        known.add(node.name)
        index = index + 1

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

    def __get_struct_members(self, elem):
        members = []
        kname = elem.attributes["name"].value
        ktype = elem.attributes["type"].value
        if elem.getElementsByTagName('dimension'):
            dimension = dict(elem.getElementsByTagName('dimension')[0].attributes.items())
            if "isVariableSize" in dimension:
                type = dimension.get("variableSizeFieldType", "u32")
                name = dimension.get("variableSizeFieldName", kname + "_len")
                members.append(model.StructMember(name, type, None, None, None))
                members.append(model.StructMember(kname, ktype, True, name, None))
            elif "size" in dimension:
                size = dimension["size"]
                members.append(model.StructMember(kname, ktype, True, None, size))
        else:
            members.append(model.StructMember(kname, ktype, None, None, None))
        return members

    def __get_struct(self, elem):
        name = elem.attributes["name"].value
        members = reduce(lambda x, y: x + y, (self.__get_struct_members(member)
                                              for member
                                              in elem.getElementsByTagName('member')), [])
        return model.Struct(name, members)

    def __get_structs(self, dom):
        return [self.__get_struct(elem)
                for elem
                in dom.getElementsByTagName("struct") + dom.getElementsByTagName("message")
                if elem.hasChildNodes()]

    def __get_enum_member(self, elem):
        value = elem.getAttribute('value')
        value = value if value != "-1" else "0xFFFFFFFF"
        return model.EnumMember(elem.attributes["name"].value, value)

    def __get_enum(self, elem):
        name = elem.attributes["name"].value
        members = [self.__get_enum_member(member) for member in elem.getElementsByTagName('enum-member')]
        return model.Enum(name, members)

    def __get_enums(self, dom):
        return [self.__get_enum(elem) for elem in dom.getElementsByTagName('enum') if elem.hasChildNodes()]

    def __union_parse(self, tree_node):
        union_dict = {}
        enum_dict = {}

        union_nodes = tree_node.getElementsByTagName('union')
        for union_element in union_nodes:
            name = union_element.getAttribute('name')
            union = model.UnionHolder()
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
            return model.Typedef(elem.attributes["name"].value, elem.attributes["type"].value)
        elif elem.hasAttribute("primitiveType"):
            type = self.primitive_types[elem.attributes["primitiveType"].value]
            return model.Typedef(elem.attributes["name"].value, type)

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

    def __get_model(self, dom):
        mdl = model.Model()
        mdl.constants = self.__get_constants(dom)
        mdl.typedefs = self.__get_typedefs(dom)
        mdl.enums = self.__get_enums(dom)
        mdl.structs = sort_struct(self.__get_structs(dom))
        mdl.includes = self.__get_includes(dom)
        mdl.union_dict, enums = self.__union_parse(dom)
        mdl.enums += enums.items()
        return mdl

    def parse_string(self, string):
        return self.__get_model(xml.dom.minidom.parseString(string))

    def parse(self, file):
        return self.__get_model(xml.dom.minidom.parse(file))
