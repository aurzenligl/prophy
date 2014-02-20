from collections import namedtuple

class Holder(object):

    def __init__(self):
        self.list=[]
    def add_to_list(self,element_name,element_value=0):
        pass
    def get_list(self):
        return self.list
    def get_list_len(self):
        return len(self.list)
class IncludeHolder(Holder):

    def __init__(self):
        self.list=[]

    def add_to_list(self,element):
        self.list.append(element)

class EnumHolder(Holder):

    def __init__(self):
        self.list=[]
        self.enum=namedtuple('enum','enum_name enum_value')
        self.special={}

    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.enum(element_name,element_value))


class ConstantHolder(Holder):

    def __init__(self):
        self.list=[]
        self.constant=namedtuple('constant','constant_name constant_value')

    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.constant(element_name,element_value))

    def __sort_list(self,list):
        out_list = []

        for t in list:
            key, val = t
            if "_" not in val:
                out_list.insert(0,(key,val))
            else:
                if (key,val) in out_list:
                    index = out_list.index((key,val))
                    out_list.insert(index + 1, (key,val))
                else:
                    out_list.append((key,val))

        return out_list

    def get_sorted_list(self):
        return self.__sort_list(self.list)

class TypeDefHolder(Holder):

    def __init__(self):
        self.list=[]
        self.typedef=namedtuple('typedef','typedef_name typedef_value')

    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.typedef(element_name,element_value))

class MemberHolder(Holder):

    def __init__(self, name, type):
        self.list=[]
        self.name = name
        self.type = type
        self.dimension=namedtuple('dimension','dimension_field_name dimension_field_value')
        self.dimension_field_name_list=[]

    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.dimension(element_name,element_value))
        self.dimension_field_name_list.append(element_name)

    def get_dimension_field_index(self,element_name):
        if element_name in self.dimension_field_name_list:
            return self.dimension_field_name_list.index(element_name)
        else:
            return -1

    def __str__(self):
        return "name="+str(self.name)+ " type="+str(self.type) + " list=" + str(len(self.list))

class MessageHolder(Holder):

    def __init__(self):
        self.list=[]
        self.name = ""

    def add_to_list(self,member):
        self.list.append(member)

    def __str__(self):
        return "name="+ self.name + "list=" + str(self.list)

class DataHolder(object):

    def __init__(self, include = IncludeHolder(), typedef = TypeDefHolder(), constant = ConstantHolder(), msgs_list =
            [],  enum_dict = {}, struct_list = [] ): 
        self.msgs_list = msgs_list
        self.enum_dict = enum_dict
        self.struct_list = struct_list
        self.include = include
        self.typedef = typedef
        self.constant = constant

    def __str__(self):
        return "msgs_list=" + str(len(self.msgs_list)) + " enum_dict=" + str(len(self.enum_dict)) + " struct_list=" + str(len(self.struct_list))

    def sort_struct(self):
        list = []
        is_base_type = 0
        index = 0
        for struct_element in self.struct_list:
            for i in xrange(struct_element.get_list_len()):
                if struct_element.list[i].type.startswith('S') or struct_element.list[i].type.startswith('U'):
                    is_base_type += 1
            if is_base_type == 0:
                list.insert(index,struct_element)
                index += 1
            else:
                list.insert(index,struct_element)
            is_base_type = 0
        return list

