import model

class StructKind:
    FIXED = 0
    DYNAMIC = 1
    UNLIMITED = 2

class ProcessedModel(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.types = {node.name: node for node in nodes}
        self.kinds = {}

        for node in nodes:
            if type(node) is model.Struct:
                if node.members:
                    if self._is_unlimited(node.members[-1]):
                        self.kinds[node.name] = StructKind.UNLIMITED
                        continue
                    if any(self._is_dynamic(member) for member in node.members):
                        self.kinds[node.name] = StructKind.DYNAMIC
                        continue
                self.kinds[node.name] = StructKind.FIXED

    def _get_struct_from_member(self, member):
        tp = self.types.get(member.type)
        while type(tp) is model.Typedef:
            tp = self.types.get(tp.type)
        if type(tp) is model.Struct:
            return tp

    def _is_unlimited_array(self, member):
        return (member.array and
                not member.array_bound and
                not member.array_size)

    def _is_dynamic_array(self, member):
        return (member.array and
                member.array_bound and
                not member.array_size)

    def _is_unlimited_struct(self, member):
        tp = self._get_struct_from_member(member)
        if tp:
            return self.kinds.get(tp.name) == StructKind.UNLIMITED
        return False

    def _is_dynamic_struct(self, member):
        tp = self._get_struct_from_member(member)
        if tp:
            return self.kinds.get(tp.name) == StructKind.DYNAMIC
        return False

    def _is_dynamic(self, member):
        return self._is_dynamic_array(member) or self._is_dynamic_struct(member)

    def _is_unlimited(self, member):
        return self._is_unlimited_array(member) or self._is_unlimited_struct(member)

    def partition(self, members):
        main = []
        parts = []
        current = main
        for member in members[:-1]:
            current.append(member)
            if self._is_dynamic(member):
                current = []
                parts.append(current)
        if members:
            current.append(members[-1])

        return main, parts
