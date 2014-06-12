import xml.etree.ElementTree as ElementTree
import model
from itertools import ifilter, islice

"""
TODO:
- arrays of u8 type should be string or bytes fields
"""

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

def make_include(elem):
    return model.Include(elem.get("href").split('.')[0])

def make_constant(elem):
    return model.Constant(elem.get("name"), elem.get("value"))

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

def make_struct_members(elem, dynamic_array = False):
    members = []
    ename = elem.get("name")
    etype = elem.get("type")
    optional = bool(elem.get("optional"))
    dimension = elem.find("dimension")
    if dimension is not None:
        size = dimension.get("size", None)
        if optional:
            members.append(model.StructMember("has_" + ename, "u32", None, None, None, False))
        if "isVariableSize" in dimension.attrib:
            type = dimension.get("variableSizeFieldType", "u32")
            name = dimension.get("variableSizeFieldName", ename + "_len")
            members.append(model.StructMember(name, type, None, None, None, False))
            members.append(model.StructMember(ename, etype, True, name, None if dynamic_array else size, False))
        else:
            members.append(model.StructMember(ename, etype, True, None, size, False))
    else:
        members.append(model.StructMember(ename, etype, None, None, None, optional))
    return members

def make_struct(elem, last_member_array_is_dynamic = False):
    if len(elem):
        members = reduce(lambda x, y: x + y, (make_struct_members(member) for member in elem[:-1]), [])
        members += make_struct_members(elem[-1], last_member_array_is_dynamic)
        return model.Struct(elem.get("name"), members)

def make_union_member(elem):
    return model.UnionMember(elem.get("name"), elem.get("type"), elem.get("discriminatorValue"))

def make_union(elem):
    if len(elem):
        return model.Union(elem.get('name'), [make_union_member(member) for member in elem])

class IsarParser(object):

    def __get_model(self, root):
        nodes = []
        nodes += [make_include(elem) for elem in filter(lambda elem: "include" in elem.tag, root.iterfind('.//*[@href]'))]
        nodes += [make_constant(elem) for elem in root.iterfind('.//constant')]
        nodes += filter(None, (make_typedef(elem) for elem in root.iterfind('.//typedef')))
        nodes += filter(None, (make_enum(elem) for elem in root.iterfind('.//enum')))
        nodes += filter(None, (make_struct(elem) for elem in root.iterfind('.//struct')))
        nodes += filter(None, (make_union(elem) for elem in root.iterfind('.//union')))
        nodes += filter(None, (make_struct(elem, last_member_array_is_dynamic = True) for elem in root.iterfind('.//message')))
        return nodes

    def parse_string(self, string):
        return self.__get_model(ElementTree.fromstring(string))

    def parse(self, file):
        return self.__get_model(ElementTree.parse(file))

