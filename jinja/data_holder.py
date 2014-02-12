from collections import namedtuple


class DataHolder(object):
    msgs_list=[]
    enum_dict=[]
    struct_list=[]

    def __init(self):
        self.include=IncludeHolder()
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


class Holder(object):

    list=[]

    def add_to_list(self,element_name,element_value=0):
        pass
    def get_list(self):
        return self.list

class IncludeHolder(Holder):

    def add_to_list(self,element):
        self.list.append(element)

class EnumHolder(Holder):

    enum=namedtuple('enum','enum_name enum_value')

    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.enum(element_name,element_value))


class ConstantHolder(Holder):

    constant=namedtuple('constant','constant_name constant_value')

    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.constant(element_name,element_value))

    def __sort_list(self,list):
        pass

    def get_sorted_list(self,list):
        return __sort_list(self,list)

class TypeDefHolder(Holder):

    typedef=namedtuple('typedef','typedef_name typedef_value')

    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.typedef(element_name,element_value))

class Member(Holder):

    name=''
    type=''
    list=[]
    dimension=namedtuple('dimension','dimension_field_name dimension_field_value')
    def add_to_list(self,element_name,element_value = 0):
        self.list.append(self.typedef(element_name,element_value))







# my proposal for new Data_Holder class
# class DataHolder(object):
#     def __init__(self, include, enum, constants):
#         self.dic = {"include" : include, "enum": enum, "constants" : constants }

