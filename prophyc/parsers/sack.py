import os
import re
import ctypes.util
from .clang.cindex import Config, Index, CursorKind, TypeKind, TranslationUnitLoadError, LibclangError

from prophyc import model

unambiguous_builtins = {
    TypeKind.UCHAR: 'u8',
    TypeKind.SCHAR: 'i8',
    TypeKind.CHAR_S: 'i8',
    TypeKind.POINTER: 'u32',
    TypeKind.FLOAT: 'r32',
    TypeKind.DOUBLE: 'r64',
    TypeKind.BOOL: 'i32'
}

class SackParserError(Exception):
    pass

class SackModel(object):
    def __init__(self, included_isar_supples=[]):
        self.known = set()
        self.nodes = []
        list(map(self.add_node, included_isar_supples))
        self.names_defined_in_isar = list(SackModel.get_node_names(included_isar_supples))

    def add_node(self, node):
        self.known.add(node.name)
        self.nodes.append(node)

    @staticmethod
    def get_node_names(nodes_list):
        for node in nodes_list:
            if isinstance(node, model.Include):
                for name in SackModel.get_node_names(node.nodes):
                    yield name
            else:
                yield node.name

class Builder(object):

    def __init__(self, tree_model, parsed_file_content):
        self.tree = tree_model
        self.content = parsed_file_content

    @staticmethod
    def alphanumeric_name(cursor):
        name = cursor.type.spelling.decode()
        if name.startswith('struct '):
            name = name.replace('struct ', '', 1)
        elif name.startswith('enum '):
            name = name.replace('enum ', '', 1)
        elif name.startswith('union '):
            name = name.replace('union ', '', 1)
        return re.sub('[^0-9a-zA-Z_]+', '__', name)

    def get_type_name_of_missing_declaration(self, cursor):
        spelling = cursor.spelling
        spelling_len = len(spelling) if spelling else 0
        decl_start, decl_end = cursor.extent.start.offset, cursor.extent.end.offset
        return self.content[decl_start:decl_end - spelling_len].decode().strip()

    def get_type_name(self, tp, cursor):
        decl = tp.get_declaration()

        def dive_deeper(method):
            name = Builder.alphanumeric_name(decl)
            if name not in self.tree.known:
                method(decl)
            return name

        if tp.kind is TypeKind.TYPEDEF:
            return self.get_type_name(decl.underlying_typedef_type, cursor)
        elif tp.kind in (TypeKind.UNEXPOSED, TypeKind.ELABORATED, TypeKind.RECORD):

            if decl.kind in (CursorKind.STRUCT_DECL, CursorKind.CLASS_DECL):
                return dive_deeper(self.add_struct)

            elif decl.kind is CursorKind.UNION_DECL:
                return dive_deeper(self.add_union)

            elif decl.kind is CursorKind.ENUM_DECL:
                return self.get_type_name(decl.type, cursor)

            elif decl.kind is CursorKind.TYPEDEF_DECL:
                return self.get_type_name(decl.underlying_typedef_type, cursor)

            else:
                raise SackParserError("Unknown declaration")

        elif tp.kind in (TypeKind.CONSTANTARRAY, TypeKind.INCOMPLETEARRAY):
            return self.get_type_name(tp.element_type, cursor)

        elif tp.kind is TypeKind.ENUM:
            return dive_deeper(self.add_enum)

        if decl.kind is CursorKind.NO_DECL_FOUND and cursor:
            name = self.get_type_name_of_missing_declaration(cursor)
            if name in self.tree.names_defined_in_isar:
                return name

        if tp.kind in (TypeKind.USHORT, TypeKind.UINT, TypeKind.ULONG, TypeKind.ULONGLONG):
            return 'u%d' % (tp.get_size() * 8)

        elif tp.kind in (TypeKind.SHORT, TypeKind.INT, TypeKind.LONG, TypeKind.LONGLONG):
            return 'i%d' % (tp.get_size() * 8)

        return unambiguous_builtins[tp.kind]

    def add_enum(self, cursor):
        def enum_member(cursor):
            name = cursor.spelling.decode()
            value = cursor.enum_value
            if value < 0:
                value = "0x%X" % (0x100000000 + value)
            else:
                value = str(value)
            return model.EnumMember(name, value)

        members = [enum_member(x) for x in cursor.get_children()]
        node = model.Enum(Builder.alphanumeric_name(cursor), members)
        self.tree.add_node(node)

    def add_struct(self, cursor):
        def array_length(tp):
            if tp.kind is TypeKind.CONSTANTARRAY:
                return tp.element_count
            return None

        def struct_member(cursor_):
            name = cursor_.spelling.decode()
            type_name = self.get_type_name(cursor_.type, cursor_)
            array_len = array_length(cursor_.type)
            return model.StructMember(name, type_name, size=array_len)

        members = [struct_member(x) for x in cursor.get_children()
                   if x.kind is CursorKind.FIELD_DECL and not x.is_bitfield()]
        node = model.Struct(Builder.alphanumeric_name(cursor), members)
        self.tree.add_node(node)

    def add_union(self, cursor):
        def union_member(cursor, disc):
            name = cursor.spelling.decode()
            type_name = self.get_type_name(cursor.type, cursor)
            return model.UnionMember(name, type_name, str(disc))

        members = [union_member(x, i) for i, x in enumerate(cursor.get_children())
                   if x.kind is CursorKind.FIELD_DECL]
        node = model.Union(Builder.alphanumeric_name(cursor), members)
        self.tree.add_node(node)

def build_model(tu, tree, content):
    builder = Builder(tree, content)
    for cursor in tu.cursor.get_children():
        if cursor.kind is CursorKind.UNEXPOSED_DECL:
            for in_cursor in cursor.get_children():
                if in_cursor.kind is CursorKind.STRUCT_DECL and in_cursor.spelling and in_cursor.is_definition():
                    builder.add_struct(in_cursor)
        if cursor.spelling and cursor.is_definition():
            if cursor.kind is CursorKind.STRUCT_DECL:
                builder.add_struct(cursor)
            if cursor.kind is CursorKind.ENUM_DECL:
                builder.add_enum(cursor)


class SackParser(object):

    @staticmethod
    def check():
        class SackParserStatus(object):
            def __init__(self, error = None):
                self.error = error

            def __bool__(self):
                return not bool(self.error)

            __nonzero__ = __bool__

        def _check_libclang():
            testconf = Config()
            try:
                testconf.get_cindex_library()
                return True
            except LibclangError:
                return False

        import platform
        if platform.python_implementation() == 'PyPy':
            return SackParserStatus("sack input doesn't work under PyPy due to ctypes incompatibilities")
        if not _check_libclang():
            return SackParserStatus("sack input requires libclang and it's not installed")
        return SackParserStatus()

    def __init__(self, include_dirs=[], warn=None, supple_nodes=[]):
        self.include_dirs = include_dirs
        self.warn = warn
        self.supple_nodes = supple_nodes

    def parse(self, content, path, _):
        args_ = ["-I" + x for x in self.include_dirs]

        index = Index.create()
        path = path.encode()
        content = content.encode()
        tree = SackModel(self.supple_nodes)

        try:
            tu = index.parse(path, args_, unsaved_files=((path, content),))
        except TranslationUnitLoadError:
            raise model.ParseError([(path.decode(), 'error parsing translation unit')])

        if self.warn:
            unknown_type_name_warning_prog = re.compile("unknown type name '(\w+)'")
            for diag in tu.diagnostics:
                spelling = diag.spelling.decode()
                match = unknown_type_name_warning_prog.search(spelling)
                if not match or match.group(1) not in tree.names_defined_in_isar:
                    self.warn(spelling, location=SackParser._get_location(diag.location))

        build_model(tu, tree, content)
        return tree.nodes

    @staticmethod
    def _get_location(location):
        return '%s:%s:%s' % (location.file.name.decode(), location.line, location.column)


def _setup_libclang():
    if os.environ.get('PROPHY_NOCLANG'):
        Config.set_library_file('prophy_noclang')
        return

    versions = [None, '3.5', '3.4', '3.3', '3.2', '3.6', '3.7', '3.8', '3.9']
    for v in versions:
        name = v and 'clang-' + v or 'clang'
        libname = ctypes.util.find_library(name)
        if libname:
            Config.set_library_file(libname)
            break


_setup_libclang()
