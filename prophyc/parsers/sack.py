import re
from clang.cindex import Index, CursorKind, TypeKind

from prophyc import model

unambiguous_builtins = {
    TypeKind.UCHAR: 'u8',
    TypeKind.SCHAR: 'i8',
    TypeKind.CHAR_S: 'i8',
    TypeKind.POINTER: 'u32',
    TypeKind.FLOAT: 'r32',
    TypeKind.DOUBLE: 'r64',
    TypeKind.BOOL: 'u32'
}

def alphanumeric_name(cursor):
    return re.sub('[^0-9a-zA-Z_]+', '__', cursor.type.spelling)

def get_enum_member(cursor):
    name = cursor.spelling
    value = cursor.enum_value
    if value < 0:
        value = "0x%X" % (0x100000000 + value)
    else:
        value = str(value)
    return model.EnumMember(name, value)

class Builder(object):
    def __init__(self):
        self.known = set()
        self.nodes = []

    def _add_node(self, node):
        self.known.add(node.name)
        self.nodes.append(node)

    def _get_field_array_len(self, tp):
        if tp.kind is TypeKind.CONSTANTARRAY:
            return tp.element_count
        return None

    def _build_field_type_name(self, tp):
        if tp.kind is TypeKind.TYPEDEF:
            return self._build_field_type_name(tp.get_declaration().underlying_typedef_type)
        elif tp.kind in (TypeKind.UNEXPOSED, TypeKind.RECORD):
            decl = tp.get_declaration()
            if decl.kind in (CursorKind.STRUCT_DECL, CursorKind.CLASS_DECL):
                name = alphanumeric_name(decl)
                if name not in self.known:
                    self.add_struct(decl)
                return name
            elif decl.kind is CursorKind.UNION_DECL:
                name = alphanumeric_name(decl)
                if name not in self.known:
                    self.add_union(decl)
                return name
            elif decl.kind is CursorKind.ENUM_DECL:
                return self._build_field_type_name(decl.type)
            else:
                raise Exception("Unknown declaration")
        elif tp.kind in (TypeKind.CONSTANTARRAY, TypeKind.INCOMPLETEARRAY):
            return self._build_field_type_name(tp.element_type)
        elif tp.kind is TypeKind.ENUM:
            decl = tp.get_declaration()
            name = alphanumeric_name(decl)
            if name not in self.known:
                self.add_enum(decl)
            return name

        if tp.kind in (TypeKind.USHORT, TypeKind.UINT, TypeKind.ULONG, TypeKind.ULONGLONG):
            return 'u%d' % (tp.get_size() * 8)
        elif tp.kind in (TypeKind.SHORT, TypeKind.INT, TypeKind.LONG, TypeKind.LONGLONG):
            return 'i%d' % (tp.get_size() * 8)

        return unambiguous_builtins[tp.kind]

    def _build_struct_member(self, cursor):
        name = cursor.spelling
        type_name = self._build_field_type_name(cursor.type)
        array_len = self._get_field_array_len(cursor.type)
        is_array = None if array_len is None else True
        return model.StructMember(name, type_name, size = array_len)

    def _build_union_member(self, cursor, disc):
        name = cursor.spelling
        type_name = self._build_field_type_name(cursor.type)
        return model.UnionMember(name, type_name, str(disc))

    def add_enum(self, cursor):
        members = map(get_enum_member, cursor.get_children())
        node = model.Enum(alphanumeric_name(cursor), members)
        self._add_node(node)

    def add_struct(self, cursor):
        members = [self._build_struct_member(x)
                   for x in cursor.get_children()
                   if x.kind is CursorKind.FIELD_DECL and not x.is_bitfield()]
        node = model.Struct(alphanumeric_name(cursor), members)
        self._add_node(node)

    def add_union(self, cursor):
        members = [self._build_union_member(x, i)
                   for i, x in enumerate(cursor.get_children())
                   if x.kind is CursorKind.FIELD_DECL]
        node = model.Union(alphanumeric_name(cursor), members)
        self._add_node(node)

def build_model(tu):
    builder = Builder()
    for cursor in tu.cursor.get_children():
        if cursor.kind is CursorKind.UNEXPOSED_DECL:
            for in_cursor in cursor.get_children():
                if in_cursor.kind is CursorKind.STRUCT_DECL and in_cursor.spelling and in_cursor.is_definition():
                    builder.add_struct(in_cursor)
        if cursor.kind is CursorKind.STRUCT_DECL and cursor.spelling and cursor.is_definition():
            builder.add_struct(cursor)
    return builder.nodes

class SackParser(object):
    def __init__(self, include_dirs = []):
        self.include_dirs = include_dirs

    def parse(self, filename):
        args_ = [filename] + ["-I" + x for x in self.include_dirs]
        index = Index.create()
        tu = index.parse(None, args_)
        return build_model(tu)
