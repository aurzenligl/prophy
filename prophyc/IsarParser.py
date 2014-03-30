# -*- coding: utf-8 -*-

import xml.dom.minidom
import xml.etree.ElementTree as ElementTree
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
                model.Union: get_union_deps}

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

def make_include(elem):
    return model.Include(elem.get("href").split('.')[0])

def make_constant(elem):
    return model.Constant(elem.get("name"), elem.get("value"))

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

def make_typedef(elem):
    if "type" in elem.attrib:
        return model.Typedef(elem.get("name"), elem.get("type"))
    elif "primitiveType" in elem.attrib:
        return model.Typedef(elem.get("name"), primitive_types[elem.get("primitiveType")])

def make_enum_member(elem):
    value = elem.get('value')
    value = value if value != "-1" else "0xFFFFFFFF"
    return model.EnumMember(elem.get("name"), value)

def make_enum(elem):
    if len(elem):
        return model.Enum(elem.get("name"), [make_enum_member(member) for member in elem])

node_makers = {"{http://www.nsn.com/2008/XInclude}include": make_include,
               "{http://www.w3.org/2001/XInclude}include": make_include,
               "constant": make_constant,
               "typedef": make_typedef,
               "enum": make_enum}

# #         "typedef",
# #         "enum",
# #         "struct",
# #         "message",
# #         "union"}

def make_node(elem):
    return node_makers[elem.tag](elem)

class IsarParser(object):

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

    def __get_union_member(self, elem):
        return model.UnionMember(elem.getAttribute("name"), elem.getAttribute("type"))

    def __get_union(self, elem):
        name = elem.getAttribute('name')
        members = [self.__get_union_member(member) for member in elem.getElementsByTagName("member")]
        return model.Union(name, members)

    def __get_unions(self, dom):
        return [self.__get_union(elem) for elem in dom.getElementsByTagName('union')]

    def __get_model(self, dom, root):
        nodes = []

        known = set(node_makers.keys())
        nodes += filter(None, [make_node(elem) for elem in filter(lambda elem: elem.tag in known, root.findall('.//'))])

        nodes += self.__get_structs(dom)
        nodes += self.__get_unions(dom)
        dependency_sort(nodes)
        return nodes

    def parse_string(self, string):
        return self.__get_model(xml.dom.minidom.parseString(string), ElementTree.fromstring(string))

    def parse(self, file):
        return self.__get_model(xml.dom.minidom.parse(file), ElementTree.parse(file))
