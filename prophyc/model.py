from collections import namedtuple

Include = namedtuple("Include", ["name"])

Constant = namedtuple("Constant", ["name", "value"])

Typedef = namedtuple("Typedef", ["name", "type"])

Enum = namedtuple("Enum", ["name", "members"])
EnumMember = namedtuple("EnumMember", ["name", "value"])

Struct = namedtuple("Struct", ["name", "members"])

class StructMember(object):

    def __init__(self, name, type,
                 bound = None, size = None,
                 unlimited = False, optional = False):
        assert(sum((bool(bound or size), unlimited, optional)) <= 1)

        self.name = name
        self.type = type
        self.array = bool(bound or size or unlimited)
        self.bound = bound
        self.size = size
        self.optional = optional

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        fmts = {
            (False, False, False, False): '{0} {1}',
            (True, False, True, False): '{0} {1}[{3}]',
            (True, True, False, False): '{0} {1}<>({2})',
            (True, True, True, False): '{0} {1}<{3}>({2})',
            (True, False, False, False): '{0} {1}<...>',
            (False, False, False, True): '{0}* {1}'
        }
        fmt = fmts[(self.array, bool(self.bound), bool(self.size), self.optional)]
        return fmt.format(self.type, self.name, self.bound, self.size)

Union = namedtuple("Union", ["name", "members"])
UnionMember = namedtuple("UnionMember", ["name", "type", "discriminator"])
