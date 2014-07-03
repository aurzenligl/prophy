import model

class StructKind:
    FIXED = 0
    DYNAMIC = 1
    UNLIMITED = 2

class ProcessedNodes(object):

    def __init__(self, nodes):
        self.nodes = nodes
        self.types = {node.name: node for node in nodes}
        self.kinds = {}

        for node in nodes:
            if type(node) is model.Struct:
                if node.members:
                    if self.is_unlimited(node.members[-1]):
                        self.kinds[node.name] = StructKind.UNLIMITED
                        continue
                    if any(self.is_dynamic(member) for member in node.members):
                        self.kinds[node.name] = StructKind.DYNAMIC
                        continue
                self.kinds[node.name] = StructKind.FIXED

    def _is_unlimited_array(self, member):
        return (member.array and
                not member.array_bound and
                not member.array_size)

    def _is_dynamic_array(self, member):
        return (member.array and
                member.array_bound and
                not member.array_size)

    def get_kind(self, member):
        tp = self.types.get(member.type)
        while type(tp) is model.Typedef:
            tp = self.types.get(tp.type)
        if type(tp) is model.Struct:
            return self.kinds.get(tp.name, StructKind.FIXED)
        else:
            return StructKind.FIXED

    def is_dynamic(self, member):
        return (self._is_dynamic_array(member) or
                self.get_kind(member) == StructKind.DYNAMIC)

    def is_unlimited(self, member):
        return (self._is_unlimited_array(member) or
                self.get_kind(member) == StructKind.UNLIMITED)

    def partition(self, members):
        main = []
        parts = []
        current = main
        for member in members[:-1]:
            current.append(member)
            if self.is_dynamic(member):
                current = []
                parts.append(current)
        if members:
            current.append(members[-1])

        return main, parts
