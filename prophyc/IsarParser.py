import xml.etree.ElementTree as ElementTree
import model
from itertools import ifilter, islice

"""
TODO:
- arrays of u8 type should be string or bytes fields
"""

def get_include_deps(include):
    """
        Function uses in sorting, return empty list
        because include elements have not dependences

        :param include: has one filed "name"
        :type include: namedtuple

        :return: empty list
        :rtype: list
    """
    return []

def get_constant_deps(constant):
    """
        Function uses in sorting, return elements
        which have depending with other constant

        :param constant: has two fields: name, value
        :type constant: namedtuple

        :return: list with constant elements, which are not digit
        :rtype: list
    """
    return filter(lambda x: not x.isdigit(),
                  reduce(lambda x, y: x.replace(y, " "), "()+-", constant.value).split())

def get_typedef_deps(typedef):
    """
        Function uses in sorting, from typedef we need only type of fields

        :param typedef: has two fields: name, value
        :type typedef: namedtuple

        :return: list with type of typedef
        :type: list
    """
    return [typedef.type]

def get_enum_deps(enum):
    """
        Function uses in sorting, return empty list
        because enum elements have not dependences

        :param enum: has two elements: name, members - namedtuple
        :type enum: namedtuple

        :return: empty list
        :rtype: list
    """
    return []

def get_struct_deps(struct):
    """
        Function uses in sorting, return list with type of struct members
        because struct members could have dependences

        :param struct: has two elements: name, members - namedtuple
        :type struct:  namedtuple

        :return: list with type of struct members
        :rtype: list
    """
    return [member.type for member in struct.members]

def get_union_deps(union):
    """
        Function uses in sorting, return list with type of union members
        because union members could have dependences

        :param union: has two elements: name, members - namedtuple
        :param type: namedtuple

        :return: list with type of union members
        :rtype: list
    """
    return [member.type for member in union.members]

def get_deps(node):
    """
    Get suitable function in dependency of node type
    and return results od this function
    """
    return deps_visitor[type(node)](node)

deps_visitor = {model.Include: get_include_deps,
                model.Constant: get_constant_deps,
                model.Typedef: get_typedef_deps,
                model.Enum: get_enum_deps,
                model.Struct: get_struct_deps,
                model.Union: get_union_deps}

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
    """
    Function which sorts all of elements from namedtuples
        :param nodes: contain all nodes from xml
        :type nodes: list
    """
    import pdb; pdb.set_trace()
    known = set(x + y for x in "uir" for y in ["8", "16", "32", "64"])
    available = set(node.name for node in nodes)

    index = 0
    max_index = len(nodes)

    while index < max_index:
        if not dependency_sort_rotate(nodes, known, available, index):
            index = index + 1

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
    """
    Extract data of include element and write to namedtuple of include elements
        :param elem: object with row from xml with node named include
        :type elem: xml.etree.ElementTree

        :return: object with extracted data
        :rtype: namedtuple
    """
    return model.Include(elem.get("href").split('.')[0])

def make_constant(elem):
    """
    Extract data of constant element and write to named tuple of constant elements
        :param elem: object with row from xml with constant
        :type elem: xml.etree.ElementTree

        :return: object with extracted data
        :rtype: namedtuple
    """
    return model.Constant(elem.get("name"), elem.get("value"))

def make_typedef(elem):
    """
    Extract data of typedef element and write to namedtuple of typedef elements
        :param elem: object with row from xml with typedef
        :type elem: xml.etree.ElementTree

        :return: object with extracted data
        :rtype: namedtuple
    """
    if "type" in elem.attrib:
        return model.Typedef(elem.get("name"), elem.get("type"))
    elif "primitiveType" in elem.attrib:
        return model.Typedef(elem.get("name"), primitive_types[elem.get("primitiveType")])

def make_enum_member(elem):
    """
    Extract data of enum member write to namedtuple of enum members
        :param elem: object with row from xml with enum member
        :type elem: xml.etree.ElementTree

        :return: object with extracted data
        :rtype: namedtuple
    """
    value = elem.get('value')
    value = value if value != "-1" else "0xFFFFFFFF"
    return model.EnumMember(elem.get("name"), value)

def make_enum(elem):
    """
    Make complete enum with all members, for each one of enum member
    is called function make_enum_member
        :param elem: object with rows from xml with complete enum
        :type elem: xml.etree.ElementTree

        :return: object with extracted data
        :rtype: namedtuple
    """
    if len(elem):
        return model.Enum(elem.get("name"), [make_enum_member(member) for member in elem])

def make_struct_members(elem, dynamic_array = False):
    """
    Extract information from fields of struct or messages
        :param elem: object with rows from xml with struct member
        :type elem: xml.etree.ElementTree
        :param dynamic_array: parameter is true when we use this function on message struct
        :type dynamic_array: bool

        :return: list with namedtuple object with extracted data
        :type: list
    """
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
    """
    Extract information about struct or messages, for all members is called function make_strcut_member
        :param elem: object with xml rows about struct
        :type elem: xml.etree.ElementTree

        :param last_member_array_is_dynamic: True when we use this function on message struct
        :type last_member_array_is_dynamic: bool

        :return: object with extracted data
        :type: namedtuple
    """
    if len(elem):
        members = reduce(lambda x, y: x + y, (make_struct_members(member) for member in elem[:-1]), [])
        members += make_struct_members(elem[-1], last_member_array_is_dynamic)
        return model.Struct(elem.get("name"), members)

def make_union_member(elem):
    """
    Extract data of union member write to namedtuple of union members
        :param elem: object with row from xml with union member
        :type elem: xml.etree.ElementTree

        :return: object with extracted data
        :rtype: namedtuple
    """
    return model.UnionMember(elem.get("name"), elem.get("type"), elem.get("discriminatorValue"))

def make_union(elem):
    """
    Extract information about union, for all members is called function make_union_member
        :param elem: object with xml rows about union
        :type elem: xml.etree.ElementTree

        :return: object with extracted data
        :type: namedtuple
    """
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
        dependency_sort(nodes)
        return nodes

    def parse_string(self, string):
        """
        Parses string with xml structure
            :param string: string with xml syntax to parse

            :return: list with namedtuples with all nodes from string
            :rtype: list
        """
        return self.__get_model(ElementTree.fromstring(string))

    def parse(self, file):
        """
        Parses xml file
            :param file: object of xml file

            :return: list contained namedtuples with all nodes from string
            :rtype: list
        """
        return self.__get_model(ElementTree.parse(file))

    def post_patch(self, nodes):
        """
        Function calls dependency dependency_sort function
        """
        dependency_sort(nodes)
