from collections import namedtuple

class Holder(object):

    def __init__(self):
        self.list = []
    def add_to_list(self, element_name, element_value = 0):
        pass
    def get_list(self):
        return self.list
    def get_list_len(self):
        return len(self.list)

class UnionHolder(Holder):

    def __init__(self):
        self.list = []
        self.union = namedtuple('union', 'union_type union_name')
        self.special = {}

    def add_to_list(self, member_type, member_name):
        self.list.append(self.union(member_type, member_name))

Include = namedtuple("Include", ["name"])

Constant = namedtuple("Constant", ["name", "value"])

Typedef = namedtuple("Typedef", ["name", "type"])

Enum = namedtuple("Enum", ["name", "members"])
EnumMember = namedtuple("EnumMember", ["name", "value"])

Struct = namedtuple("Struct", ["name", "members"])
StructMember = namedtuple("StructMember", ["name", "type", "array", "array_bound", "array_size"])

class Model(object):

    def __init__(self):
        self.nodes = []

        self.union_dict = {}

    def __str__(self):
        return "msgs_list=" + str(len(self.msgs_list)) + " enum_dict=" + str(len(self.enum_dict)) + " struct_list=" + str(len(self.struct_list))
