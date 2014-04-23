from clang.cindex import Index, CursorKind, TypeKind
import model

""" tests: """
""" prepend with typedefed struct """
""" prepend with namespaced struct """
""" prepend with enum """
""" prepend with union """

class Builder(object):
    def __init__(self):
        self.known = set()
        self.nodes = []

    def _add_node(self, node):
        self.known.add(node.name)
        self.nodes.append(node)

    def _get_field_array_len(self, cursor):
        return None

    def _build_field_type_name(self, cursor):
        # ... add needed enums, structs, unions if not known
        return 'u32'

    def _build_struct_member(self, cursor):
        name = cursor.spelling
        type_name = self._build_field_type_name(cursor)
        array_len = self._get_field_array_len(cursor)
        is_array = None if array_len is None else True
        return model.StructMember(name, type_name, is_array, array_len, None, None)

    def add_struct(self, cursor):
        members = [self._build_struct_member(x)
                   for x in cursor.get_children()
                   if x.kind is CursorKind.FIELD_DECL]
        node = model.Struct(cursor.spelling, members)
        self._add_node(node)

def build_model(tu):
    builder = Builder()
    for cursor in tu.cursor.get_children():
        if cursor.kind is CursorKind.STRUCT_DECL and cursor.spelling:
            builder.add_struct(cursor)
    return builder.nodes

class SackParser(object):
    def __init__(self, include_dirs = []):
        self.include_dirs = include_dirs

    def parse(self, filename):
        args_ = [filename, '-m32'] + ["-I" + x for x in self.include_dirs]
        index = Index.create()
        tu = index.parse(None, args_)
        return build_model(tu)
