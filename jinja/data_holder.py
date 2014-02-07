
class data_holder(object):
    msg_dict = {}
    typedef_dict = {}
    constant_dict = {}
    enum_dict = {}
    struct_dict = {}

    def  __init__(self,msg_dict,typedef_dict,constant_dict,enum_dict,struct_dict):
        self.set_dicts(msg_dict,typedef_dict,constant_dict,enum_dict,struct_dict)

    def set_dicts(self,msg_dict,typedef_dict,constant_dict,enum_dict,struct_dict):
        self.msg_dict =msg_dict
        self.typedef_dict =typedef_dict
        self.constant_dict =constant_dict
        self.enum_dict =enum_dict
        self.struct_dict =struct_dict

    def return_dicts_as_list(self):
        if self.msg_dict == 0:
            return (self.msg_dict,self.typedef_dict,self.constant_dict,self.enum_dict,self.struct_dict)

msg_dict={}
typedef_dict={}
constant_dict={}
enum_dict={}
struct_dict={}

data=data_holder(msg_dict,typedef_dict,constant_dict,enum_dict,struct_dict)
print data.return_dicts_as_list()
