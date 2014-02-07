
class data_holder(object):

    msg_dict = {}
    typedef_dict = {}
    constant_dict = {}
    enum_dict = {}
    struct_dict = {}

    def set_dicts(self,msg_dict,typedef_dict,constant_dict,enum_dict,struct_dict):
        self.msg_dict = msg_dict
        self.typedef_dict = typedef_dict
        self.constant_dict = constant_dict
        self.enum_dict = enum_dict
        self.struct_dict = struct_dict

    def return_dicts(self):
        if self.msg_dict == 0:
            return self.msg_dict,self.typedef_dict,self.constant_dict,self.enum_dict,self.struct_dict

