from collections import namedtuple

#class DataHolder(object):
#    msg_dict={}
#    typedef_dict={}
#    constant_dict={}
#    enum_dict={}
#    struct_dict={}

#    def sort_list(self, dic):
#        out_list = []

#        for key, val in dic.iteritems():
#            if "_" not in val:
#                out_list.insert(0,key)
#            else:
#                if val in out_list:
#                    index = out_list.index(val)
#                    out_list.insert(index + 1, key)
#                else:
#                    out_list.append(key)
#        return out_list


class Holder(object):

    def add_to_list(self,element_name,element_value=0):
        pass
    def get_list_values(self):
        pass

class IncludeHolder(Holder):

    include_list = []

    def add_to_list(self,element):
        self.include_list.append(element)

    def get_list_values(self):
        return self.include_list

class EnumHolder(Holder):

    name=''
    enum=namedtuple('enum','enum_name enum_value')
    enum_list = []

    def __init__(self,name):
        self_name=name

    def add_to_list(self,element_name,element_value = 0):
        self.enum_list.append(self.enum(element_name,element_value))

    def get_list_values(self):
        return self.enum_list

    def get_enum_holder_name(self):
        return self.name

class ConstantHolder(Holder):

    constant=namedtuple('constant','constant_name constant_value')
    constant_list = []

    def add_to_list(self, element_name,element_value = 0):
        self.constant_list.append(self.constant(element_name, element_value))

    def get_list_values(self):
        return self.constant_list


# my proposal for new Data_Holder class
class DataHolder(object):
    def __init__(self, include, enum, constants):
        self.dic = {"include" : include, "enum": enum, "constants" : constants }

