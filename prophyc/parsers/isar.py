import os
import xml.etree.ElementTree as ElementTree

from prophyc import model, six
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
    first = string_[open_pos + 1: comma_pos].strip()
    second = string_[comma_pos + 1: close_pos].strip()
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


def make_include(xml_elem, process_file, warn):
    if "include" in xml_elem.tag:
        path = xml_elem.get("href")
        try:
            nodes = process_file(path)
        except (CyclicIncludeError, FileNotFoundError) as e:
            if warn:
                warn(str(e))
            nodes = []
        return model.Include(os.path.splitext(path)[0], nodes, docstring=get_docstr(xml_elem))


def get_docstr(xml_elem):
    return six.decode_string(xml_elem.get("comment", "")) or None


def make_constant(xml_elem):
    return model.Constant(
        xml_elem.get("name"),
        expand_operators(xml_elem.get("value")),
        docstring=get_docstr(xml_elem)
    )


def make_typedef(xml_elem):
    if "type" in xml_elem.attrib:
        return model.Typedef(
            xml_elem.get("name"),
            xml_elem.get("type"),
            docstring=get_docstr(xml_elem)
        )

    elif "primitiveType" in xml_elem.attrib and xml_elem.get("name") not in primitive_types.values():
        return model.Typedef(
            xml_elem.get("name"),
            primitive_types[xml_elem.get("primitiveType")],
            docstring=get_docstr(xml_elem)
        )


def make_enum(xml_elem):
    def check_for_duplicates(enum_obj):
        values = set()
        for m in enum_obj.members:
            if m.value in values:
                raise ValueError("Duplicate Enum value in '{}', value '{}'.".format(enum_obj.name, m.value))
            values.add(m.value)

    if len(xml_elem):
        members = []
        for member in xml_elem:
            value = member.get('value')
            try:
                int_value = int(value, 0)
                if int_value < 0:
                    value = "0x{:X}".format(0x100000000 + int_value)
            except ValueError:
                pass
            members.append(model.EnumMember(
                member.get("name"),
                expand_operators(value),
                docstring=get_docstr(member))
            )

        enum = model.Enum(xml_elem.get("name"), members, docstring=get_docstr(xml_elem))
        check_for_duplicates(enum)
        return enum


def make_struct_members(xml_elem, dynamic_array=False):
    xml_elem_name = xml_elem.get("name")
    xml_elem_type = xml_elem.get("type")
    optional = xml_elem.get("optional")
    optional = bool(optional) and optional.lower() == "true"
    dimension = xml_elem.find("dimension")
    comment = get_docstr(xml_elem)

    def collect():
        if dimension is None:
            yield model.StructMember(xml_elem_name, xml_elem_type, optional=optional, docstring=comment)
        else:
            size = dimension.get("size", None)
            size2 = dimension.get("size2", None)
            if size2:
                size = "{}*{}".format(size, size2)
            if optional:
                yield model.StructMember("has_" + xml_elem_name, "u32", docstring="implicit enabler for optional field")

            sizer_name = dimension.get("variableSizeFieldName", None)
            if sizer_name and "@" in sizer_name[0]:
                yield model.StructMember(xml_elem_name, xml_elem_type, bound=sizer_name[1:], docstring=comment)

            elif size and "THIS_IS_VARIABLE_SIZE_ARRAY" in size:
                sizer_name = "numOf" + xml_elem_name[0].upper() + xml_elem_name[1:]
                yield model.StructMember(xml_elem_name, xml_elem_type, bound=sizer_name, docstring=comment)

            elif "isVariableSize" in dimension.attrib:
                type_ = dimension.get("variableSizeFieldType", "u32")
                sizer_name = dimension.get("variableSizeFieldName", xml_elem_name + "_len")
                yield model.StructMember(sizer_name, type_, docstring=comment)
                size_ = None if dynamic_array else size
                yield model.StructMember(xml_elem_name, xml_elem_type, bound=sizer_name, size=size_, docstring=comment)

            else:
                yield model.StructMember(xml_elem_name, xml_elem_type, size=size, docstring=comment)

    return list(collect())


def make_struct(xml_elem, last_member_array_is_dynamic=False):
    if len(xml_elem):
        members = []
        for member in xml_elem:
            for sub_ in make_struct_members(member, last_member_array_is_dynamic):
                members.append(sub_)
        return model.Struct(xml_elem.get("name"), members, docstring=get_docstr(xml_elem))


def make_union(xml_elem):
    if len(xml_elem):
        members = []
        for member in xml_elem:
            members.append(model.UnionMember(
                member.get("name"),
                member.get("type"),
                member.get("discriminatorValue"),
                docstring=get_docstr(member),
            ))
        return model.Union(xml_elem.get('name'), members, docstring=get_docstr(xml_elem))


class IsarParser(object):

    def __init__(self, warn=None):
        self.warn = warn

    def parse(self, content, _, process_file):
        # by default FileProcessor decodes files while opening in _process_file method,
        # but ElementTree doesn't like it. ElementTree handles the encoding on its own,
        # so it's OK to encode the data back into utf-8 before parsing
        content = content.encode('utf-8')

        def collect():
            root = ElementTree.fromstring(content)
            for xml_elem in root.iterfind('.//*[@href]'):
                yield make_include(xml_elem, process_file, self.warn)

            for xml_elem in root.iterfind('.//constant'):
                yield make_constant(xml_elem)

            for xml_elem in root.iterfind('.//typedef'):
                yield make_typedef(xml_elem)

            for xml_elem in root.iterfind('.//enum'):
                yield make_enum(xml_elem)

            for xml_elem in root.iterfind('.//struct'):
                yield make_struct(xml_elem)

            for xml_elem in root.iterfind('.//union'):
                yield make_union(xml_elem)

            for xml_elem in root.iterfind('.//message'):
                yield make_struct(xml_elem, last_member_array_is_dynamic=True)

        return [element for element in collect() if element]
