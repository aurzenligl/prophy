import os
import re
import ctypes.util
from .clang.cindex import Config, Index, CursorKind, TypeKind, TranslationUnitLoadError, LibclangError

from prophyc import model
from prophyc.generators.cpp import _generate_def_enum
from contextlib import contextmanager

class SackParserError(Exception):
    pass

class SackModelTree(object):
    def __init__(self):
        self.known = set()
        self.nodes = []

    def add_node(self, node):
        self.known.add(node.name)
        self.nodes.append(node)

    def remove_nodes(self, node_names_to_remove):
        self.nodes = [node for node in self.nodes if node.name not in node_names_to_remove]
        self.known -= set(node_names_to_remove)

class Builder(object):
    unambiguous_builtins = {
        TypeKind.UCHAR: 'u8',
        TypeKind.SCHAR: 'i8',
        TypeKind.CHAR_S: 'i8',
        TypeKind.POINTER: 'u32',
        TypeKind.FLOAT: 'r32',
        TypeKind.DOUBLE: 'r64',
        TypeKind.BOOL: 'i32'
    }

    def __init__(self, tree_model):
        self.tree = tree_model

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

    def get_type_name(self, tp):
        decl = tp.get_declaration()

        def dive_deeper(method):
            name = Builder.alphanumeric_name(decl)
            if name not in self.tree.known:
                method(decl)
            return name

        if tp.kind is TypeKind.TYPEDEF:
            return self.get_type_name(decl.underlying_typedef_type)

        elif tp.kind in (TypeKind.UNEXPOSED, TypeKind.ELABORATED, TypeKind.RECORD):

            if decl.kind in (CursorKind.STRUCT_DECL, CursorKind.CLASS_DECL):
                return dive_deeper(self.add_struct)

            elif decl.kind is CursorKind.UNION_DECL:
                return dive_deeper(self.add_union)

            elif decl.kind is CursorKind.ENUM_DECL:
                return self.get_type_name(decl.type)

            elif decl.kind is CursorKind.TYPEDEF_DECL:
                return self.get_type_name(decl.underlying_typedef_type)

            else:
                raise SackParserError("Unknown declaration, {} {}".format(tp.spelling, decl.kind))

        elif tp.kind in (TypeKind.CONSTANTARRAY, TypeKind.INCOMPLETEARRAY):
            return self.get_type_name(tp.element_type)

        elif tp.kind is TypeKind.ENUM:
            return dive_deeper(self.add_enum)

        if tp.kind in (TypeKind.USHORT, TypeKind.UINT, TypeKind.ULONG, TypeKind.ULONGLONG):
            return 'u%d' % (tp.get_size() * 8)

        elif tp.kind in (TypeKind.SHORT, TypeKind.INT, TypeKind.LONG, TypeKind.LONGLONG):
            return 'i%d' % (tp.get_size() * 8)

        return self.unambiguous_builtins[tp.kind]

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
            type_name = self.get_type_name(cursor_.type)
            array_len = array_length(cursor_.type)
            return model.StructMember(name, type_name, size=array_len)

        members = [struct_member(x) for x in cursor.get_children()
                   if x.kind is CursorKind.FIELD_DECL and not x.is_bitfield()]
        node = model.Struct(Builder.alphanumeric_name(cursor), members)
        self.tree.add_node(node)

    def add_union(self, cursor):
        def union_member(cursor, disc):
            name = cursor.spelling.decode()
            type_name = self.get_type_name(cursor.type)
            return model.UnionMember(name, type_name, str(disc))

        members = [union_member(x, i) for i, x in enumerate(cursor.get_children())
                   if x.kind is CursorKind.FIELD_DECL]
        node = model.Union(Builder.alphanumeric_name(cursor), members)
        self.tree.add_node(node)

    def build_model(self, translation_unit):
        for cursor in translation_unit.cursor.get_children():
            if cursor.kind is CursorKind.UNEXPOSED_DECL:
                for in_cursor in cursor.get_children():
                    if in_cursor.kind is CursorKind.STRUCT_DECL and in_cursor.spelling and in_cursor.is_definition():
                        self.add_struct(in_cursor)
            if cursor.spelling and cursor.is_definition():
                if cursor.kind is CursorKind.STRUCT_DECL:
                    self.add_struct(cursor)
                if cursor.kind is CursorKind.ENUM_DECL:
                    self.add_enum(cursor)

class SupplementaryDefs(object):

    def __init__(self, include_tree):

        self.include_tree = include_tree
        self.stub_names = [node.name for node in SupplementaryDefs.flatten_nodes(include_tree)]
        self.stub_defs = SupplementaryDefs.prepare_stubs(include_tree)
        self.stubs_lines_count = len(self.stub_defs)

    @staticmethod
    def flatten_nodes(nodes_list):
        for node in nodes_list:
            if isinstance(node, model.Include):
                for node in SupplementaryDefs.flatten_nodes(node.nodes):
                    yield node
            else:
                yield node

    @staticmethod
    def unique_nodes(include_tree):
        picked = []
        for node in SupplementaryDefs.flatten_nodes(include_tree):
            if node.name not in picked:
                picked.append(node.name)
                yield node

    @staticmethod
    def prepare_stubs(include_tree):
        def create_stub_definition(node):
            if isinstance(node, model.Constant):
                yield "#define {} {}".format(node.name, node.value)
            elif isinstance(node, model.Enum):
                for line in _generate_def_enum(node).split('\n'):
                    # need to have all lines separated to know its count
                    yield line
            else:
                yield "struct {} {{}};".format(node.name)

        flatten_nodes = SupplementaryDefs.unique_nodes(include_tree)
        return [line for node in flatten_nodes for line in create_stub_definition(node)]

    def prepend_stubs(self, content):
        if not self.stub_defs:
            return content
        return '\n'.join(self.stub_defs) + '\n' + content

    @contextmanager
    def implicit_supplementation(self, parsed_content):
        enriched_content = self.prepend_stubs(parsed_content)

        sack_tree = SackModelTree()
        for include_node in self.include_tree:
            sack_tree.add_node(include_node)

        yield enriched_content, sack_tree

        sack_tree.remove_nodes(self.stub_names)


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

    def __init__(self, include_dirs=[], warn=None, include_tree=[]):
        self.include_dirs = include_dirs
        self.warn = warn
        self.supples = SupplementaryDefs(include_tree)

    def parse(self, content, path, _):
        args_ = ["-I" + x for x in self.include_dirs]
        index = Index.create()
        with self.supples.implicit_supplementation(content) as (content_, tree):
            builder = Builder(tree)
            path = path.encode()
            content_ = content_.encode()

            try:
                translation_unit = index.parse(path, args_, unsaved_files=((path, content_),))
            except TranslationUnitLoadError:
                raise model.ParseError([(path.decode(), 'error parsing translation unit')])

            self.print_diagnostics(path, translation_unit)
            builder.build_model(translation_unit)

        return tree.nodes

    def print_diagnostics(self, path, translation_unit):
        if self.warn:
            for diag in translation_unit.diagnostics:
                spelling = diag.spelling.decode()
                location = self._get_location(diag.location, path)
                self.warn(spelling, location)

    def _get_location(self, location, target_path):
        location_file = location.file.name.decode()
        target_file_name = os.path.basename(target_path.decode())
        if os.path.basename(location_file) == target_file_name:
            stubs_len = self.supples.stubs_lines_count
            is_in_stubs = location.line < stubs_len
            stubs_file = "supplementary_defs_in_{}".format(target_file_name)
            location_line = location.line if is_in_stubs else (location.line - stubs_len)
            location_file = location_file if not is_in_stubs else stubs_file

        else:
            location_line = location.line
        return '%s:%s:%s' % (location_file, location_line, location.column)


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
