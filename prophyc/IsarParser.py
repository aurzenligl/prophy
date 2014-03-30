# -*- coding: utf-8 -*-

import xml.dom.minidom
import model
from itertools import ifilter, islice

"""
TODO:
- nodes should be read in order that they really appear in xml file,
  not all includes, then all typedefs, then all enums, etc.
  lxml library allows to do just that (+ it's faster than dom)
- arrays of u8 type should be string or bytes fields
"""

def get_include_deps(include):
    return []

def get_constant_deps(constant):
    return filter(lambda x: not x.isdigit(),
                  reduce(lambda x, y: x.replace(y, " "), "()+-", constant.value).split())

def get_typedef_deps(typedef):
    return [typedef.type]

def get_enum_deps(enum):
    return []

def get_struct_deps(struct):
    return [member.type for member in struct.members]

def get_union_deps(union):
    return [member.type for member in union.members]

deps_visitor = {model.Include: get_include_deps,
                model.Constant: get_constant_deps,
                model.Typedef: get_typedef_deps,
                model.Enum: get_enum_deps,
                model.Struct: get_struct_deps,
                model.Union: get_union_deps, }

def get_deps(node):
    return deps_visitor[type(node)](node)

def dependency_sort_rotate(nodes, known, available, index):
    node = nodes[index]
    for dep in get_deps(node):
        if dep not in known and dep in available:
            found = next(ifilter(lambda x: x.name == dep, islice(nodes, index + 1, None)))
            found_index = nodes.index(found)
            nodes.insert(index, nodes.pop(found_index))
            return True
    known.add(node.name)
    return False

def dependency_sort(nodes):
    known = set(x + y for x in "uir" for y in ["8", "16", "32", "64"])
    available = set(node.name for node in nodes)

    index = 0
    max_index = len(nodes)

    while index < max_index:
        if not dependency_sort_rotate(nodes, known, available, index):
            index = index + 1

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

    def __get_union_member(self, elem):
        return model.UnionMember(elem.getAttribute("name"), elem.getAttribute("type"))

    def __get_union(self, elem):
        name = elem.getAttribute('name')
        members = [self.__get_union_member(member) for member in elem.getElementsByTagName("member")]
        return model.Union(name, members)

    def __get_unions(self, dom):
        return [self.__get_union(elem) for elem in dom.getElementsByTagName('union')]

    def __get_typedef(self, elem):
        if elem.hasAttribute("type"):
            return model.Typedef(elem.attributes["name"].value, elem.attributes["type"].value)
        elif elem.hasAttribute("primitiveType"):
            type = self.primitive_types[elem.attributes["primitiveType"].value]
            return model.Typedef(elem.attributes["name"].value, type)

    def __get_typedefs(self, dom):
        return filter(None, (self.__get_typedef(elem) for elem in dom.getElementsByTagName('typedef')))

    def __get_constant(self, elem):
        return model.Constant(elem.attributes["name"].value, elem.attributes["value"].value)

    def __get_constants(self, dom):
        return [self.__get_constant(elem) for elem in dom.getElementsByTagName('constant')]

    def __get_includes(self, dom):
        return [model.Include(elem.attributes["href"].value.split('.')[0])
                for elem
                in dom.getElementsByTagName("xi:include")]

    def __get_model(self, dom):
        nodes = []
        nodes += self.__get_includes(dom)
        nodes += self.__get_constants(dom)
        nodes += self.__get_typedefs(dom)
        nodes += self.__get_enums(dom)
        nodes += self.__get_structs(dom)
        nodes += self.__get_unions(dom)
        dependency_sort(nodes)
        return nodes

    def parse_string(self, string):
        return self.__get_model(xml.dom.minidom.parseString(string))

    def parse(self, file):
        return self.__get_model(xml.dom.minidom.parse(file))
