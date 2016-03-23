import os
import xml.etree.ElementTree as ElementTree

from ..six import reduce
from prophyc import model
from prophyc.file_processor import CyclicIncludeError, FileNotFoundError

def extract_operator_args(string_, pos):
    brackets = 0
    open_pos = pos
    comma_pos = pos
    close_pos = pos
    for i, char in enumerate(string_[pos:]):
        if char == '(':
            brackets += 1
            if brackets == 1:
                open_pos += i
        elif char == ',':
            if brackets == 1:
                comma_pos += i
        elif char == ')':
            brackets -= 1
            if not brackets:
                close_pos += i
                break
    first = string_[open_pos + 1 : comma_pos].strip()
    second = string_[comma_pos + 1 : close_pos].strip()
    return pos, close_pos + 1, first, second

operators = (
    ('shiftLeft(', '<<'),
    ('bitMaskOr(', '|')
)

def expand_operators(string_):
    for operator in operators:
        while True:
            pos = string_.find(operator[0])
            if pos == -1:
                break
            open_pos, close_pos, arg1, arg2 = extract_operator_args(string_, pos)
            string_ = string_[:open_pos] + '(({}) {} ({}))'.format(arg1, operator[1], arg2) + string_[close_pos:]
    return string_

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

def make_include(elem, process_file, warn):
    path = elem.get("href")
    try:
        nodes = process_file(path)
    except (CyclicIncludeError, FileNotFoundError) as e:
        if warn:
            warn(str(e))
        nodes = []
    return model.Include(os.path.splitext(path)[0], nodes)

def make_constant(elem):
    return model.Constant(elem.get("name"), expand_operators(elem.get("value")))

def make_typedef(elem):
    if "type" in elem.attrib:
        return model.Typedef(elem.get("name"), elem.get("type"))
    elif "primitiveType" in elem.attrib and elem.get("name") not in primitive_types.values():
        return model.Typedef(elem.get("name"), primitive_types[elem.get("primitiveType")])

def make_enum_member(elem):
    value = elem.get('value')
    value = value if value != "-1" else "0xFFFFFFFF"
    return model.EnumMember(elem.get("name"), expand_operators(value))

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
        if "size2" in dimension.attrib:
            size = "{}*{}".format(size, dimension.get("size2", None))
        if optional:
            members.append(model.StructMember("has_" + ename, "u32"))

        sizer_name = dimension.get("variableSizeFieldName", None)
        if sizer_name and "@" in sizer_name[0]:
            members.append(model.StructMember(ename, etype, bound = sizer_name[1:]))

        elif size and "THIS_IS_VARIABLE_SIZE_ARRAY" in size:
            sizer_name = "numOf" + ename[0].upper() + ename[1:]
            members.append(model.StructMember(ename, etype, bound = sizer_name))

        elif "isVariableSize" in dimension.attrib:
            type_ = dimension.get("variableSizeFieldType", "u32")
            sizer_name = dimension.get("variableSizeFieldName", ename + "_len")
            members.append(model.StructMember(sizer_name, type_))
            members.append(model.StructMember(ename, etype, bound = sizer_name, size = None if dynamic_array else size))
        else:
            members.append(model.StructMember(ename, etype, size = size))
    else:
        members.append(model.StructMember(ename, etype, optional = optional))
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

    def __init__(self, warn = None):
        self.warn = warn

    def __get_model(self, root, process_file):
        nodes = []
        nodes += [make_include(elem, process_file, self.warn) for elem in filter(lambda elem: "include" in elem.tag, root.iterfind('.//*[@href]'))]
        nodes += [make_constant(elem) for elem in root.iterfind('.//constant')]
        nodes += filter(None, (make_typedef(elem) for elem in root.iterfind('.//typedef')))
        nodes += filter(None, (make_enum(elem) for elem in root.iterfind('.//enum')))
        nodes += filter(None, (make_struct(elem) for elem in root.iterfind('.//struct')))
        nodes += filter(None, (make_union(elem) for elem in root.iterfind('.//union')))
        nodes += filter(None, (make_struct(elem, last_member_array_is_dynamic = True) for elem in root.iterfind('.//message')))
        return nodes

    def parse(self, content, path, process_file):
        return self.__get_model(ElementTree.fromstring(content), process_file)
