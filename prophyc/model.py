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

class Struct(object):
    Member = namedtuple("Member", ["name", "type", "array", "array_bound", "array_size"])

    def __init__(self):
        self.name = ""
        self.members = []

    def __str__(self):
        return "name=" + self.name + "members=" + str(self.members)

class DataHolder(object):

    def __init__(self):
        self.structs = []

        """ list of strings, e.g. "externals" """
        self.includes = []

        """ list of name-members pairs, where member is list of name-value pairs
            e.g. ("EEnum", [(EEnum_Value1, 1), (EEnum_Value2, 2)]) """
        self.enums = []

        """ list of name-type pairs, e.g. ("TMyTypedef", "u32") """
        self.typedefs = []

        """ list of name-value pairs, e.g. ("CONST", 10) """
        self.constants = []

        self.union_dict = {}

    def __str__(self):
        return "msgs_list=" + str(len(self.msgs_list)) + " enum_dict=" + str(len(self.enum_dict)) + " struct_list=" + str(len(self.struct_list))
