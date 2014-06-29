import model

class StructKind:
    FIXED = 0
    DYNAMIC = 1
    UNLIMITED = 2

def build_types(nodes):
    return {node.name: node for node in nodes}

def build_kinds(types, nodes):
    kinds = {}

    def is_unlimited_array(member):
        return (member.array and
                not member.array_bound and
                not member.array_size)

    def is_dynamic_array(member):
        return (member.array and
                member.array_bound and
                not member.array_size)

    def _get_struct_from_member(member):
        tp = types.get(member.type)
        while type(tp) is model.Typedef:
            tp = types.get(tp.type)
        if type(tp) is model.Struct:
            return tp

    def is_unlimited_struct(member):
        tp = _get_struct_from_member(member)
        if tp:
            return kinds.get(tp.name) == StructKind.UNLIMITED
        return False

    def is_dynamic_struct(member):
        tp = _get_struct_from_member(member)
        if tp:
            return kinds.get(tp.name) == StructKind.DYNAMIC
        return False

    for node in nodes:
        if type(node) is model.Struct:
            if node.members:
                if (is_unlimited_array(node.members[-1]) or
                        is_unlimited_struct(node.members[-1])):
                    kinds[node.name] = StructKind.UNLIMITED
                    continue
                if any((is_dynamic_array(member) or
                            is_dynamic_struct(member))
                       for member in node.members):
                    kinds[node.name] = StructKind.DYNAMIC
                    continue
            kinds[node.name] = StructKind.FIXED

    return kinds

def _partition(types, kinds, members):

    def is_dynamic_array(member):
        return (member.array and
                member.array_bound and
                not member.array_size)

    def _get_struct_from_member(member):
        tp = types.get(member.type)
        while type(tp) is model.Typedef:
            tp = types.get(tp.type)
        if type(tp) is model.Struct:
            return tp

    def is_dynamic_struct(member):
        tp = _get_struct_from_member(member)
        if tp:
            return kinds.get(tp.name) == StructKind.DYNAMIC
        return False

    def is_dynamic(member):
        return is_dynamic_array(member) or is_dynamic_struct(member)

    main = []
    parts = []
    current = main
    for member in members[:-1]:
        current.append(member)
        if is_dynamic(member):
            current = []
            parts.append(current)
    if members:
        current.append(members[-1])

    return main, parts

class ProcessedModel(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.types = build_types(nodes)
        self.kinds = build_kinds(self.types, nodes)

    def partition(self, members):
        return _partition(self.types, self.kinds, members)
