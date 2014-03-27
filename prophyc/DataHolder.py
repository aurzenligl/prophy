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

class MemberHolder(Holder):

    def __init__(self, name, type):
        self.list = []
        self.name = name
        self.type = type
        self.dimension = namedtuple('dimension', 'dimension_field_name dimension_field_value')
        self.dimension_field_name_list = []

    def add_to_list(self, element_name, element_value = 0):
        self.list.append(self.dimension(element_name, element_value))
        self.dimension_field_name_list.append(element_name)

    def get_dimension_field_index(self, element_name):
        if element_name in self.dimension_field_name_list:
            return self.dimension_field_name_list.index(element_name)
        else:
            return -1

    def __str__(self):
        return "name=" + str(self.name) + " type=" + str(self.type) + " list=" + str(len(self.list))

class MessageHolder(Holder):

    def __init__(self):
        self.list = []
        self.name = ""
        self.base_type = 0
    def __is_base_type(self, member):
        if member.type.startswith('S'):
            self.base_type = 1
    def add_to_list(self, member):
        self.__is_base_type(member)
        if self.message_type == 0:
            self.list.insert(0, member)
        else:
            self.list.append(member)
    def message_type(self):
        return self.base_type
    def __str__(self):
        return "name=" + self.name + "list=" + str(self.list)

def _get_struct_name_and_index(struct_list, struct_dict):
    for x in struct_list:
        index = struct_list.index(x)
        struct_dict[x.name] = index

def _sorter(struct_list, index, out_list, struct_dict, lista):
    element = struct_list[index]
    element_name = element.name
    for member_elem in element.get_list():
        member_type = member_elem.type
        if member_type.startswith('S') and member_type in struct_dict:
            index = struct_dict[member_type]
            x = struct_list[index]
            if x not in out_list:
                out_list.extend(_sorter(struct_list, index, out_list, struct_dict, lista))
        else:
            for x in struct_list:
                if member_type in x.name:
                    if x not in out_list:
                        out_list.append(x)
    if element not in out_list:
        out_list.append(element)
    return lista

class DataHolder(object):

    def __init__(self):
        self.msgs_list = []
        self.struct_list = []

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
        # self.struct_dict = {}

    def __str__(self):
        return "msgs_list=" + str(len(self.msgs_list)) + " enum_dict=" + str(len(self.enum_dict)) + " struct_list=" + str(len(self.struct_list))

    def sort_struct(self):
        struct_list = self.struct_list
        index = 0
        out_list = []
        struct_dict = {}
        lista = []
        _get_struct_name_and_index(struct_list, struct_dict)
        for struct_elem_index in xrange(len(struct_list)):
            out_list.extend(_sorter(struct_list, struct_elem_index, out_list, struct_dict, lista))
        return out_list
