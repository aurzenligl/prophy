from collections import namedtuple

class Holder(object):
    list=[]
    def add_to_list(self,element_name,element_value=0):
        pass
    def get_list(self):
        return self.list

class IncludeHolder(Holder):
    list = []
    def add_to_list(self,element):
        self.list.append(element)

class EnumHolder(Holder):
    list = []
    enum=namedtuple('enum','enum_name enum_value')
    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.enum(element_name,element_value))

class ConstantHolder(Holder):
    list =[]
    constant=namedtuple('constant','constant_name constant_value')
    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.constant(element_name,element_value))
    def __sort_list(self,list):
        pass
    def get_sorted_list(self,list):
        return __sort_list(self,list)

class TypeDefHolder(Holder):
    list =[]
    typedef=namedtuple('typedef','typedef_name typedef_value')
    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.typedef(element_name,element_value))

class MemberHolder(Holder):
    name=''
    type=''
    list=[]
    dimension=namedtuple('dimension','dimension_field_name dimension_field_value')
    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.dimension(element_name,element_value))

class MessageHolder(Holder):
    list = []
    def add_to_list(self,member):
        self.list.append(member)

class DataHolder(object):
    msgs_list=[]
    enum_dict={}
    struct_list=[]

    def __init__(self, include = IncludeHolder()):
        self.include = include
        self.typedef=TypeDefHolder()
        self.constant=ConstantHolder()

    def sort_list(self, dic):
        out_list = []
        for key, val in dic.iteritems():
            if "_" not in val:
                out_list.insert(0,key)
            else:
                if val in out_list:
                    index = out_list.index(val)
                    out_list.insert(index + 1, key)
                else:
                    out_list.append(key)
        return out_list
